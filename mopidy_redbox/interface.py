import time
import serial
import os
import json
from threading import Thread
import logging
from transitions import Machine, State, MachineError

from mopidy.exceptions import FrontendError

import mopidy_redbox

from microparcel import microparcel as mp

from protocol.REDBoxMsg import REDBoxMsg
from protocol.REDBoxMasterRouter import REDBoxMasterRouter


logger = logging.getLogger(__name__)


class SerialInterfaceListener(Thread, REDBoxMasterRouter):
    def __init__(self, core, config):
        super(SerialInterfaceListener, self).__init__()

        self._stop_flag = False

        self.core = core

        self._data_path = os.path.join(mopidy_redbox.Extension.get_data_dir(config), b'data.json')



        self._curr_played_position = 0


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
                State('podcast'), 
            ], 
            transitions=[
                { 'trigger': 'power_off', 'source': '*', 'dest': 'turn_off' },

                { 'trigger': 'press_radio', 'source': ['podcast', 'radio'], 'dest': 'radio' },
                { 'trigger': 'press_podcast', 'source': ['podcast', 'radio'], 'dest': 'podcast' },

                { 'trigger': 'tuner', 'source': 'radio', 'dest': 'radio', 'after':'set_radio' },
                { 'trigger': 'tuner', 'source': 'podcast', 'dest': 'podcast', 'after':'set_podcast' },

                { 'trigger': 'volume', 'source': '*', 'dest': None, 'after':'set_volume' },
            
                { 'trigger': 'next_radio_bank', 'source': 'radio', 'dest':None, 'after':'set_next_radio_bank'},
                { 'trigger': 'previous_radio_bank', 'source': 'radio', 'dest':None, 'after':'set_previous_radio_bank'},

                { 'trigger': 'next_podcast', 'source': 'podcast', 'dest': 'podcast', 'after':'set_next_in_podcast' },
                { 'trigger': 'previous_podcast', 'source': 'podcast', 'dest': 'podcast', 'after':'set_previous_in_podcast' },
            ], 
            initial='podcast'
        )

    def initLibrary(self):
        # {position:Ref}
        self.lib = {
            "podcasts":{},
            "radio_banks":{}
        }

        # Load podcasts from lib
        podcasts = self.core.library.browse("redbox:podcasts").get()
        self.lib['podcasts'] = {int(pod.uri.split(":")[-1]):pod for pod in podcasts}
        
        
        # Load radios from lib
        banks = self.core.library.browse("redbox:radios").get()
        for bank in banks:
            radios = self.core.library.browse(bank.uri).get()
            self.lib["radio_banks"][bank.name] = {int(radio.uri.split(':')[-1]):radio for radio in radios}
        

        # load default bank
        self._radio_bank = None
        if not os.path.isfile(self._data_path) and len(self.lib["radio_banks"]) > 0:
            with open(self._data_path, 'w') as fp:
                json.dump({"bank":self.lib["radio_banks"].keys()[0]}, fp)

        if os.path.isfile(self._data_path):
            with open(self._data_path) as fp:
                data = json.load(fp)
                self._radio_bank = data['bank']


    def initCommunication(self, serial_port, serial_baudrate):
        # opening serial port
        try:
            # rtscts=True,dsrdtr=True is for virtual port (using socat)
            self.serial = serial.Serial(serial_port, serial_baudrate, timeout=0.1, rtscts=False, dsrdtr=False)
        except Exception as e:
            raise FrontendError("Impossible to open serial port {}: {}".format(serial_port, str(e)))

        self._parser = mp.make_parser_cls(REDBoxMsg().size)()



    def run(self):
        while not self.stop:
            ser_in = self.serial.read()
            if ser_in == "":
                continue

            raw_byte = ord(ser_in)

            msg = REDBoxMsg()

            # parse byte
            status = self._parser.parse(raw_byte, msg)
            if status == self._parser.Status.Complete:
                self.process(msg)
            if status == self._parser.Status.Error:
                logger.error("Error in parsing Serial Message: recv byte = {}, current msg = {}".format(raw_byte, msg.data))

        self.serial.close()



    def find_closest_playable(self, raw_pos, positions, margin=3 ):
        def distance(val, target):
            return abs(val-target)

        valid_positions = [p for p in positions if distance(raw_pos, p) <= margin]
        if len(valid_positions) == 1:
            return valid_positions[0]
        elif len(valid_positions) > 1:
            pos_sorted = sorted(valid_positions, key=lambda pos: distance(raw_pos, pos))
            return pos_sorted[0]

        return None


    ####################################################################
    ################### Serial Message Implementation  #################
    ####################################################################
    def processPotentiometerVolume(self, in_potentiometervalue):
        position = int(100*(float(in_potentiometervalue) / 32767.0))
        self.volume(position=position)

    def processPotentiometerTuner(self, in_potentiometervalue):
        position = int(100*(float(in_potentiometervalue) / 32767.0))
        self.tuner(position=position)

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

        self.core.mixer.set_volume(position)

    def set_radio(self, position=None):
        """
            @paramn position: volume, between 0 and 100
        """
        if self._radio_bank is None:
            logger.warning("No bank selected...")
            return


        radios = self.lib["radio_banks"][self._radio_bank]

        found_pos = self.find_closest_playable(position, radios.keys())
        if found_pos is not None:
            if self._curr_played_position != found_pos:
                ref_radio = radios[found_pos]
                logger.info("Playing" + str(ref_radio))
                
                self.core.tracklist.clear()
                self.core.tracklist.add(uris=[ref_radio.uri])
                self.core.playback.play(tl_track=None, tlid=None)

                self._curr_played_position = found_pos

        else:
            if self._curr_played_position != found_pos:

                self.core.tracklist.clear()
                self.core.tracklist.add(uris=["redbox:noise"])
                self.core.playback.play(tl_track=None, tlid=None)

                self._curr_played_position = found_pos


    def set_podcast(self, position=None):
        podcasts = self.lib['podcasts']

        found_pos = self.find_closest_playable(position, podcasts.keys())
        if found_pos is not None:
            if self._curr_played_position != found_pos:
                ref_pod = podcasts[found_pos]

                logger.info("Playing" + str(ref_pod))

                episodes = self.core.library.browse(ref_pod.uri).get()
                uris =  [ep.uri for ep in episodes]
                
                self.core.tracklist.clear()
                self.core.tracklist.add(uris=uris)
                self.core.playback.play(tl_track=None, tlid=None)

                self._curr_played_position = found_pos

        else:
            if self._curr_played_position != found_pos:
                
                self.core.tracklist.clear()
                self.core.tracklist.add(uris=["redbox:noise"])
                self.core.playback.play(tl_track=None, tlid=None)

                self._curr_played_position = found_pos

    def set_next_in_podcast(self, **kwargs):
        self.core.playback.next()

    def set_previous_in_podcast(self, **kwargs):
        self.core.playback.previous()

    def turn_off_system(self, **kwargs):
        pass
