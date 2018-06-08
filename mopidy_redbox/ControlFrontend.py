import pykka
import logging
import sqlite3
import serial
from mopidy import core
from mopidy.exceptions import FrontendError

        

class ControlFrontend(pykka.ThreadingActor, core.CoreListener):
    """
        Handle the input from the Arduino via serial for changing the playlist
    """
    def __init__(self, config, core):
        super(ControlFrontend, self).__init__()
        self.core = core
        self.config = config['redbox']

        self.logger = logging.getLogger(__name__)

        self.serial = serial.Serial(self.config['serial_port'], 9600, timeout=0.1)
        
        self.db = sqlite3.connect(self.config['dbfile'])
        self.radios = {}

        self.running = False


    def on_start(self):
        self.get_db_informations()
        
        try:
            self.running = True
            self.thread = Thread(target=self.thread_func)
            self.thread.start()
        except Exception as e:
            raise FrontendError("Impossible to start the thread")

    def on_stop(self):
        self.running = False
        self.thread.join()


    def thread_func(self):
        while self.running:
            raw = self.serial.readline()
            if raw == "":
                return

            splitted = raw.split("=")
            ch = splitted[0]
            val = float (splitted[1]) / 1024.0
            if(ch == "A1"):
                self.set_volume(val)
            elif(ch == "A0"):
                self.set_radio(val)
                self.curr_tuner_value = val

        self.serial.close()
        

    def set_volume(self, volume):
        v = int(volume * 100.0)
        self.core.mixer.set_volume(volume)

    def set_radio(self, position):
        def is_inside(val, target, margin):
            return val > (target-margin) and val < (target+margin)

        # self.get_db_informations()
        positions = [k for k in self.radios]

        curs_on_radio = False
        for p in positions:
            if is_inside(position, p, 0.02):
                curs_on_radio = True
                if self.radio_pos != p:
                    self.radio_pos = p

                    # self.ap_queue.put("stop")
                    # self.noise_playing = False

                    print self.radios[p]['name']
                    self.core.tracklist.clear()
                    self.core.tracklist.add(tracks=None, at_position=None, uri=self.radios[p]['uri'], uris=None)
                    self.core.tracklist.play(tl_track=None, tlid =None)
                break

        if not curs_on_radio:
            self.radio_pos = None

        if not curs_on_radio and not self.noise_playing:
        #    self.noise_playing = True
        #    self.ap_queue.put("play")

            self.core.tracklist.clear()

    def get_db_informations(self):
        self.radios = {}
        c = self.db.execute("SELECT * FROM radios")
        for e in c:
            self.radios[e[3]] = {"name":e[1], "uri":e[2]}
        print self.radios