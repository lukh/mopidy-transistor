import pykka
import logging
import sqlite3
import serial
import os
import zmq
import random
from threading import Thread

from mopidy import core
from mopidy.exceptions import FrontendError

from tools import *

context = zmq.Context()

class ControlFrontend(pykka.ThreadingActor, core.CoreListener):
    """
        Handle the input from the Arduino via serial for changing the playlist
    """
    def __init__(self, config, core):
        super(ControlFrontend, self).__init__()

        # mopidy core actor and config
        self.core = core
        self.config = config['redbox']

        # logger
        self.logger = logging.getLogger(__name__)

        # radios list from the database
        self.radios = {}

        # keep trace of the radio playing (current radio index)
        self.radio_index = None

        # raw pos for sending to the web interface
        self.raw_tuner_pos = 0.0

        # for the serial thread
        self.running = False

        self.noise_playing = False


    def on_start(self):
        # opening serial port
        try:
            self.serial = serial.Serial(self.config['serial_port'], int(self.config['serial_baudrate']), timeout=0.1)
        except Exception as e:
            raise FrontendError("Impossible to open serial port {}: {}".format(self.config['serial_port'], str(e)))
        
        # starting serial thread
        try:
            self.running = True
            self.thread_serial = Thread(target=self.thread_serial_func)
            self.thread_serial.start()
        except Exception as e:
            raise FrontendError("Impossible to start the thread: {}".format(str(e)))

        # opening webinterface thread (transmission of the current tuner pos when requested)
        try:
            self.socket_ctrl = context.socket(zmq.PUB) # used for stop signal
            self.socket_ctrl.bind("inproc://frontend_control")
            self.thread_publish = Thread(target=self.thread_webinterface_func)
            self.thread_publish.start()
        except Exception as e:
            raise FrontendError("Impossible to start the thread: {}".format(str(e)))

        

    def on_stop(self):
        # stopping serial thread
        self.running = False
        self.thread_serial.join()

        # stopping webinterface communication thread
        self.socket_ctrl.send("quit")
        self.thread_publish.join()

        self.logger.info("[Controller Frontend] Leaving")


    def thread_serial_func(self):
        """
            Acquiring serial data, parsing and dispatching:
            * volume
            * tuner
        """
        self.logger.info("[Controller Frontend] Starting thread_serial_func")
        self.db = RedBoxDataBase(self.config['dbfile'])
        self.radios = self.db.getRadiosKeywordPosition()

        while self.running:
            raw = self.serial.readline() # should be blocking ?
            if raw == "":
                continue
            
            splitted = raw.split("=")
            ch = splitted[0]
            val = round(float (splitted[1]) / 1024.0, 3)
            if(ch == "A1"):
                self.set_volume(val)
            elif(ch == "A0"):
                self.set_radio(val)
                self.raw_tuner_pos = val

        self.serial.close()
        

    def thread_webinterface_func(self):
        """
            Waiting REQ from the WebInterface, asking for tuner position.
            in a poller, another socket is listening for the stop command, from ControlFrontend, mainthread
        """
        self.logger.info("[Controller Frontend] Starting thread_webinterface_func")
        socket_tuner = context.socket(zmq.REP)
        socket_tuner.bind("ipc://tuner_position")

        socket_ctrl = context.socket(zmq.SUB)
        socket_ctrl.connect("inproc://frontend_control")
        socket_ctrl.setsockopt(zmq.SUBSCRIBE, "")

        poller = zmq.Poller()
        poller.register(socket_ctrl, zmq.POLLIN)
        poller.register(socket_tuner, zmq.POLLIN)

        while True:
            self.logger.info("[Controller Frontend] Starting thread_webinterface_func loop")
            socks = dict(poller.poll())
            if socket_ctrl in socks and socks[socket_ctrl] == zmq.POLLIN:
                msg = socket_ctrl.recv()
                if msg == "quit":
                    break

            if socket_tuner in socks and socks[socket_tuner] == zmq.POLLIN:
                msg = socket_tuner.recv()
                if msg == "query:tuner_position":
                    socket_tuner.send(str(round(self.raw_tuner_pos, 2)))
                else:
                    socket_tuner.send("unknown")

    def set_volume(self, volume):
        """
            Change volume
        """
        volume = int(volume * 100.0)
        self.logger.info("[Controller Frontend] VOLUME: {}".format(volume))
        self.core.mixer.set_volume(volume)

    def set_radio(self, position):
        """
            Select the radio or play noise if needed
        """
        def is_inside(val, target, margin):
            return val > (target-margin) and val < (target+margin)


        self.logger.info("[Controller Frontend] TUNER: {}".format(position))

        # self.get_db_informations()
        positions = [k for k in self.radios]

        curs_on_radio = False
        for p in positions:
            if is_inside(position, p, 0.01):
                curs_on_radio = True
                if self.radio_index != p:
                    self.radio_index = p

                    self.noise_playing = False

                    self.play_uri(self.radios[p].uri)

                break

        if not curs_on_radio:
            self.radio_index = None

        if not curs_on_radio and not self.noise_playing:
            self.noise_playing = True
            self.play_random_noise_from_folder()


    def play_uri(self, uri):
        """
            Plays the given uri
        """
        self.logger.info("[Controller Frontend] Playing {}".format(uri))

        self.core.tracklist.clear()
        self.core.tracklist.add(tracks=None, at_position=None, uri=uri, uris=None)
        self.core.playback.play(tl_track=None, tlid =None)

    def clear_playlist(self):
        """
            Stop playing
        """
        self.core.tracklist.clear()

    def play_random_noise_from_folder(self):
        """
            Play a random noise from the folder in config
        """
        folder = self.config['fm_noise_directory']

        # get random file in this directory
        onlyfiles = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f)) and os.path.splitext(f)[-1].lower() in [".wav", ".mp3"]]
        fn = onlyfiles[random.randint(0, len(onlyfiles)-1)]

        fn = os.path.join(folder, fn)
        if not os.path.isfile(fn):
            raise FrontendError("Noise file doesn't exists")

        uri = "file://"+fn

        self.play_uri(uri)

