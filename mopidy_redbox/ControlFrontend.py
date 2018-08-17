import pykka
import logging
import sqlite3
from transitions import Machine, State, MachineError
import serial
import os
import zmq
from subprocess import call
import random
from threading import Thread
from Queue import Queue, Empty
import podcastparser
import urllib

import time

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

        self.initStateMachine()

        # logger
        self.logger = logging.getLogger(__name__)

        # buttons and knobs map (should come from config later)
        self.control_map = {
            "A1":"volume", 
            "A0":"tuner", 

            "D0":"power_off", 
            "D1":"press_radio", 
            "D2":"press_rss", 
            "D3":"next_podcast", 
            "D4":"previous_podcast"
        }

        # radios list from the database
        self.radios = {}

        # rss lists from db
        self.podcasts = {}
        self.podcast_episode_index = None # currently played podacast

        self.update_db = False

        # keep trace of the radio playing (current radio index)
        self.radio_index = None

        # keep trace of the rss playing (current radio index)
        self.podcast_index = None

        # raw pos for sending to the web interface
        self.raw_tuner_pos = 0.0

        # for the serial thread
        self.running = False

        self.noise_playing = False

        # for com between two thread
        self.queue_ser = Queue()


    def initStateMachine(self):
        machine = Machine(
            model=self, 
            states=[
                State('turn_off', on_enter=["turn_off_system"]), 
                State('radio'), 
                State('rss'), 
            ], 
            transitions=[
                { 'trigger': 'power_off', 'source': '*', 'dest': 'turn_off' },

                { 'trigger': 'press_radio', 'source': ['rss', 'radio'], 'dest': 'radio' },
                { 'trigger': 'press_rss', 'source': ['rss', 'radio'], 'dest': 'rss' },

                { 'trigger': 'tuner', 'source': 'radio', 'dest': 'radio', 'after':'set_radio' },
                { 'trigger': 'tuner', 'source': 'rss', 'dest': 'rss', 'after':'set_podcast' },

                { 'trigger': 'volume', 'source': '*', 'dest': None, 'after':'set_volume' },
            
                { 'trigger': 'next_podcast', 'source': 'rss', 'dest': 'rss', 'after':'set_next_in_podcast' },
                { 'trigger': 'previous_podcast', 'source': 'rss', 'dest': 'rss', 'after':'set_previous_in_podcast' },
            ], 
            initial='radio'
        )


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

            self.thread_ctrl = Thread(target=self.thread_control_func)
            self.thread_ctrl.start()
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

        self.thread_ctrl.join()
        self.thread_serial.join()

        # stopping webinterface communication thread
        self.socket_ctrl.send("quit")
        self.thread_publish.join()

        self.logger.info("[Controller Frontend] Leaving")


    def thread_serial_func(self):
        self.logger.info("[Controller Frontend] Starting thread_serial_func")

        while self.running:
            raw = self.serial.readline() # blocking with given timeout in serial ctr
            if raw != "":
                self.queue_ser.put(raw)

    def thread_control_func(self):
        """
            Acquiring serial data, parsing and dispatching:
            * volume
            * tuner
        """
        self.logger.info("[Controller Frontend] Starting thread_control_func")
        self.db = RedBoxDataBase(self.config['dbfile'])
        self.radios = self.db.getRadiosKeywordPosition()
        self.podcasts = self.db.getRssFeedsKeywordPosition()

        while self.running:
            try:
                raw = self.queue_ser.get(block=False, timeout=0.2)
            except Empty:
                continue


            # raw = "Ax=YYYY" or raw = "Dx"
            splitted = raw.split('=')
            ch = splitted[0].replace("\n", "").replace("\r", "")
            val = int(splitted[1]) / 1024.0 if len(splitted) == 2 else None

            if ch in self.control_map:
                self.logger.info("[Controller Frontend] " + self.control_map[ch])
                action = self.control_map[ch]
                # validate if the action is allowed in the current state
                try:
                    self.trigger(action, position=val) # the arg position is ignored for buttons, but it is easier.
                except MachineError as e:
                    self.logger.info("[Controller Frontend] " + str(e))



            if self.update_db:
                self.update_db = False
                self.radios = self.db.getRadiosKeywordPosition()
                self.logger.info("[Controller Frontend] DB Updated")

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
                elif msg == "info:db_updated":
                    self.update_db = True
                    socket_tuner.send("ok")
                else:
                    socket_tuner.send("unknown")

    def set_volume(self, position=None):
        """
            Change volume
        """
        if position is None:
            return

        volume = int(position * 100.0)
        self.logger.info("[Controller Frontend] VOLUME: {}".format(volume))
        self.core.mixer.set_volume(volume)

    def set_radio(self, position=None):
        """
            Select the radio or play noise if needed
        """
        def is_inside(val, target, margin):
            return val > (target-margin) and val < (target+margin)

        if position is None:
            return

        self.logger.info("[Controller Frontend] TUNER: {}".format(position))

        self.raw_tuner_pos = position


        # self.get_db_informations()
        positions = [k for k in self.radios]

        curs_on_radio = False
        for p in positions:
            # looking for a match
            if is_inside(position, p, 0.01):
                curs_on_radio = True
                if self.radio_index != p:
                    self.radio_index = p

                    self.noise_playing = False

                    self.play_uri(self.radios[p].uri)
                break

            # hysteresis
            elif is_inside(position, p, 0.03):
                curs_on_radio = True
                break

        if not curs_on_radio:
            self.radio_index = None

        if not curs_on_radio and not self.noise_playing:
            self.noise_playing = True
            self.play_random_noise_from_folder()


    def set_podcast(self, position=None):
        """
            Select the RSS or play noise if needed
        """
        def is_inside(val, target, margin):
            return val > (target-margin) and val < (target+margin)

        if position is None:
            return

        self.logger.info("[Controller Frontend] TUNER: {}".format(position))

        self.raw_tuner_pos = position


        # self.get_db_informations()
        positions = [k for k in self.podcasts]

        curs_on_radio = False
        for p in positions:
            # looking for a match
            if is_inside(position, p, 0.01):
                curs_on_radio = True
                if self.podcast_index != p:
                    self.podcast_index = p

                    self.noise_playing = False

                    self.podcast_episode_index = 0
                    self.play_podcast_episode()
                break

            # hysteresis
            elif is_inside(position, p, 0.03):
                curs_on_radio = True
                break

        if not curs_on_radio:
            self.podcast_index = None
            self.podcast_episode_index = None

        if not curs_on_radio and not self.noise_playing:
            self.noise_playing = True
            self.play_random_noise_from_folder()


    def set_next_in_podcast(self, **kwargs):
        if self.podcast_index is None or self.podcast_episode_index is None:
            self.logger.info("[ControllerFrontend] No podcast selected")
            return
        self.podcast_episode_index += 1
        self.play_podcast_episode()

    def set_previous_in_podcast(self, **kwargs):
        if self.podcast_index is None or self.podcast_episode_index is None:
            self.logger.info("[ControllerFrontend] No podcast selected")
            return
        self.podcast_episode_index -= 1
        self.play_podcast_episode()




    def turn_off_system(self, **kwargs):
        self.logger.info("[ControllerFrontend] Turning off the Pi")
        call("sudo shutdown -h now", shell=True)
        

    def play_podcast_episode(self):
        def clamp(n, minn, maxn):
            return max(min(maxn, n), minn)

        if self.podcast_index is None or self.podcast_episode_index is None:
            return

        uri = self.podcasts[self.podcast_index].uri

        parsed = podcastparser.parse(uri, urllib.urlopen(uri))
        episodes = parsed['episodes']

        self.logger.info("[Controller Frontend] Accessing {} / {}".format(uri, parsed['title']))

        self.podcast_episode_index = clamp(self.podcast_episode_index, 0, len(episodes))

        episode = episodes[self.podcast_episode_index]

        self.logger.info("[Controller Frontend] Playing {}".format(episode['title']))

        # TODO check url index (?) and mime/type
        media_url = episode['enclosures'][0]['url']

        self.play_uri(media_url)



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
        if not os.path.isdir(folder):
            self.logger.warning("[Controller Frontend] Bad FM Noise folder: {}. Not playing".format(folder))
            return

        # get random file in this directory
        onlyfiles = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f)) and os.path.splitext(f)[-1].lower() in [".wav", ".mp3"]]
        if len(onlyfiles) == 0:
            self.logger.warning("[Controller Frontend] No files found in FM Noise folder: {}. Not playing".format(folder))
            return

        fn = onlyfiles[random.randint(0, len(onlyfiles)-1)]

        fn = os.path.join(folder, fn)
        if not os.path.isfile(fn):
            raise FrontendError("Noise file doesn't exists")

        uri = "file://"+fn

        self.play_uri(uri)

