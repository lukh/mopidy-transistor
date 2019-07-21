import time
import serial
from threading import Thread
from transitions import Machine, State, MachineError

from mopidy.exceptions import FrontendError

class SerialInterfaceListener(Thread):
    def __init__(self, core, config):
        super(SerialInterfaceListener, self).__init__()

        self._stop_flag = False

        self.core = core


        self.initStateMachine()
        self.initLibrary()

        # opening serial port
        try:
            # rtscts=True,dsrdtr=True is for virtual port (using socat)
            self.serial = serial.Serial(config['redbox']['serial_port'], int(config['redbox']['serial_baudrate']), timeout=0.1, rtscts=False, dsrdtr=False)
        except Exception as e:
            raise FrontendError("Impossible to open serial port {}: {}".format(config['redbox']['serial_port'], str(e)))
        
        
    @property
    def stop(self):
        return self._stop_flag

    @stop.setter
    def stop(self, st):
        self._stop_flag = st

    def run(self):
        while not self.stop:
            raw_byte = self.serial.read()
            if raw_byte == "":
                continue

            # parse byte

        self.serial.close()




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

    def initLibrary(self):
        # {position:Ref}
        self.lib = {
            "podcasts":{},
            "radio_banks":{}
        }

        podcasts = self.core.library.browse("redbox:podcasts").get()
        self.lib['podcasts'] = {int(pod.uri.split(":")[-1]):pod for pod in podcasts}
        
        
        banks = self.core.library.browse("redbox:radios").get()
        for bank in banks:
            radios = self.core.library.browse(bank.uri).get()
            self.lib["radio_banks"][bank.name] = {int(radio.uri.split(':')[-1]):radio for radio in radios}
        

    def set_volume(self, position=None):
        """
            @paramn position: volume, between 0 and 100
        """
        if position is None:
            return

        self.core.mixer.set_volume(volume)

    def set_radio(self, position=None):
        pass

    def set_podcast(self, position=None):
        pass

    def play_podcast_episode(self):
        pass

    def turn_off_system(self, **kwargs):
        pass
