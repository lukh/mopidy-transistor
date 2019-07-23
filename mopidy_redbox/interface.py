import time
import serial
from threading import Thread
import logging
from transitions import Machine, State, MachineError

from mopidy.exceptions import FrontendError

from microparcel import microparcel as mp

from protocol.REDBoxMsg import REDBoxMsg
from protocol.REDBoxMasterRouter import REDBoxMasterRouter


logger = logging.getLogger(__name__)


class SerialInterfaceListener(Thread, REDBoxMasterRouter):
    def __init__(self, core, config):
        super(SerialInterfaceListener, self).__init__()

        self._stop_flag = False

        self.core = core


        self.initStateMachine()
        self.initLibrary()
        self.initCommunication(config['redbox']['serial_port'], int(config['redbox']['serial_baudrate']))

            
        
    @property
    def stop(self):
        return self._stop_flag

    @stop.setter
    def stop(self, st):
        self._stop_flag = st


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
            
                { 'trigger': 'next_radio_bank', 'source': 'radio', 'dest':None, 'after':'set_next_radio_bank'},
                { 'trigger': 'previous_radio_bank', 'source': 'radio', 'dest':None, 'after':'set_previous_radio_bank'},

                { 'trigger': 'next_podcast', 'source': 'rss', 'dest': 'rss', 'after':'set_next_in_podcast' },
                { 'trigger': 'previous_podcast', 'source': 'rss', 'dest': 'rss', 'after':'set_previous_in_podcast' },
            ], 
            initial='radio'
        )

        self._radio_bank = None


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
        


    def initCommunication(self, serial_port, serial_baudrate):
        # opening serial port
        try:
            # rtscts=True,dsrdtr=True is for virtual port (using socat)
            self.serial = serial.Serial(serial_port, serial_baudrate, timeout=0.1, rtscts=False, dsrdtr=False)
        except Exception as e:
            raise FrontendError("Impossible to open serial port {}: {}".format(serial_port, str(e)))

        self._parser = mp.make_parser_cls(REDBoxMsg().size)



    def run(self):
        while not self.stop:
            raw_byte = self.serial.read()
            if raw_byte == "":
                continue

            msg = REDBoxMsg()

            # parse byte
            status = self._parser.parse(raw_byte, msg)
            if status == self._parser.Status.Complete:
                self.process(msg)
            if status == self._parser.Status.Error:
                logger.error("Error in parsing Serial Message: recv byte = {}, current msg = {}".format(raw_byte, msg.data))

        self.serial.close()





    ####################################################################
    ################### Serial Message Implementation  #################
    ####################################################################
    def processPotentiometerVolume(self, in_potentiometervalue):
        pass

    def processPotentiometerTuner(self, in_potentiometervalue):
        pass

    def processSwitch(self, in_switchindex, in_switchvalue):
        pass

    def processSendProtocolVersion(self, in_sendprotocolversionmajor, in_sendprotocolversionminor):
        pass

    ####################################################################
    #################### State machine calls ###########################
    ####################################################################
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
