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

            print raw_byte




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


    def set_volume(self, position=None):
        pass

    def set_radio(self, position=None):
        pass

    def set_podcast(self, position=None):
        pass

    def play_podcast_episode(self):
        pass

    def turn_off_system(self, **kwargs):
        pass
