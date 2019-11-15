import os
import pykka
import logging
import serial
import json
from threading import Thread
from queue import Queue

from transitions import Machine, State, MachineError

from mopidy import core
from mopidy.exceptions import FrontendError

import mopidy_redbox

from protocol.REDBoxMsg import REDBoxMsg
from protocol.REDBoxMasterRouter import REDBoxMasterRouter

import interface


logger = logging.getLogger(__name__)


class RedBoxFrontend(pykka.ThreadingActor, core.CoreListener, REDBoxMasterRouter):
    # used to push data to the event source (tuner, radios list, battery)
    queue_event = Queue()
    # used to communicate between front and web.
    queue_front = Queue()
    queue_web = Queue()

    def __init__(self, config, core):
        super(RedBoxFrontend, self).__init__()

        self.core = core
        self.config = config

        self._data_path = os.path.join(
            mopidy_redbox.Extension.get_data_dir(config), b'data.json')

        # the position used as a key for radio and podcast
        self._curr_played_position = 0
        # the raw position for updating when changing mode or banks
        self._curr_position = 0

    def on_start(self):
        logger.info('REDBOX Front End Running')

        self.initStateMachine()
        self.initLibrary()

        self.interface = interface.SerialInterfaceListener(
            self.actor_ref.proxy(), 
            self.config, 
            self.queue_event)
        self.interface.start()

        self.interface.sendMsg(self.makeQueryProtocolVersion())


        self.websocket = interface.WebsocketInterfaceListener(
            self.actor_ref.proxy(),
            self.queue_web
        )
        self.websocket.start()



    def on_stop(self):
        self.interface.stop = True
        self.interface.join()

        self.websocket.stop = True
        self.websocket.join()


    def initStateMachine(self):
        Machine(
            model=self,
            states=[
                State('turn_off', on_enter=["turn_off_system"]),
                State('radio'),
                State('podcast')
            ],
            transitions=[
                {'trigger': 'power_off', 'source': '*', 'dest': 'turn_off'},

                {'trigger': 'press_radio',
                    'source': ['podcast', 'radio'], 'dest': 'radio'},
                {'trigger': 'press_podcast',
                    'source': ['podcast', 'radio'], 'dest': 'podcast'},

                {'trigger': 'press_next_mode',
                    'source': 'podcast', 'dest': 'radio', 'after':'set_radio'},
                {'trigger': 'press_next_mode',
                    'source': 'radio', 'dest': 'podcast', 'after':'set_podcast'},

                {'trigger': 'tuner',
                    'source': 'radio', 'dest': 'radio', 'after': 'set_radio'},
                {'trigger': 'tuner',
                    'source': 'podcast',
                    'dest': 'podcast', 'after': 'set_podcast'},

                {'trigger': 'volume',
                    'source': '*', 'dest': None, 'after': 'set_volume'},

                {'trigger': 'next',
                    'source': ['radio', 'podcast'],
                    'dest':None, 'after':'set_next'},
                {'trigger': 'previous',
                    'source': ['radio', 'podcast'],
                    'dest':None, 'after':'set_previous'}
            ],
            initial='radio', ignore_invalid_triggers=True
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
        self._selected_radio_bank = None
        if not os.path.isfile(self._data_path) and len(self.lib["radio_banks"]) > 0:
            with open(self._data_path, 'w') as fp:
                json.dump({"bank":self.lib["radio_banks"].keys()[0]}, fp)

        if os.path.isfile(self._data_path):
            with open(self._data_path) as fp:
                data = json.load(fp)
                self._selected_radio_bank = data['bank']



    def process_queue_web(self, command):
        if command == "start_calibrate_volume_low":
            self.interface.sendMsg(
                self.makeCalibrate(
                    REDBoxMsg.CalibratePotentiometer.CalibratePotentiometer_Volume,
                    REDBoxMsg.CalibratePhase.CalibratePhase_StartLow
                )
            )
        elif command == "save_calibrate_volume_low":
            self.interface.sendMsg(
                self.makeCalibrate(
                    REDBoxMsg.CalibratePotentiometer.CalibratePotentiometer_Volume,
                    REDBoxMsg.CalibratePhase.CalibratePhase_StopLow
                )
            )
        elif command == "start_calibrate_volume_high":
            self.interface.sendMsg(
                self.makeCalibrate(
                    REDBoxMsg.CalibratePotentiometer.CalibratePotentiometer_Volume,
                    REDBoxMsg.CalibratePhase.CalibratePhase_StartHigh
                )
            )
        elif command == "save_calibrate_volume_high":
            self.interface.sendMsg(
                self.makeCalibrate(
                    REDBoxMsg.CalibratePotentiometer.CalibratePotentiometer_Volume,
                    REDBoxMsg.CalibratePhase.CalibratePhase_StopHigh
                )
            )
        elif command == "start_calibrate_tuner_low":
            self.interface.sendMsg(
                self.makeCalibrate(
                    REDBoxMsg.CalibratePotentiometer.CalibratePotentiometer_Tuner,
                    REDBoxMsg.CalibratePhase.CalibratePhase_StartLow
                )
            )
        elif command == "save_calibrate_tuner_low":
            self.interface.sendMsg(
                self.makeCalibrate(
                    REDBoxMsg.CalibratePotentiometer.CalibratePotentiometer_Tuner,
                    REDBoxMsg.CalibratePhase.CalibratePhase_StopLow
                )
            )
        elif command == "start_calibrate_tuner_high":
            self.interface.sendMsg(
                self.makeCalibrate(
                    REDBoxMsg.CalibratePotentiometer.CalibratePotentiometer_Tuner,
                    REDBoxMsg.CalibratePhase.CalibratePhase_StartHigh
                )
            )
        elif command == "save_calibrate_tuner_high":
            self.interface.sendMsg(
                self.makeCalibrate(
                    REDBoxMsg.CalibratePotentiometer.CalibratePotentiometer_Tuner,
                    REDBoxMsg.CalibratePhase.CalibratePhase_StopHigh
                )
            )
        elif command == "save":
            self.interface.sendMsg(self.makeSaveCalibration())

            
    def process_serial_message(self, msg):
        self.process(msg)


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
        logger.info("Pot Vol %d" %in_potentiometervalue)
        position = int(100*(float(in_potentiometervalue) / 32767.0))
        self.volume(position=position)

    def processPotentiometerTuner(self, in_potentiometervalue):
        logger.info("Pot Tuner %d" %in_potentiometervalue)
        position = int(100*(float(in_potentiometervalue) / 32767.0))
        self.tuner(position=position)

    def processPowerOff(self):
        logger.info("Turning Off")
        self.power_off()

    def processMode(self, in_modetype):
        logger.info("Mode %s" %str(in_modetype))
        if in_modetype == REDBoxMsg.ModeType.ModeType_NextMode:
            self.press_next_mode()
        elif in_modetype == REDBoxMsg.ModeType.ModeType_Radio:
            self.press_radio()
        elif in_modetype == REDBoxMsg.ModeType.ModeType_Podcast:
            self.press_podcast()


    def processNavigation(self, in_navigationtype):
        logger.info("Navigation %s" %(in_navigationtype))
        if in_navigationtype == REDBoxMsg.NavigationType.NavigationType_Next:
            self.next()
        elif in_navigationtype == REDBoxMsg.NavigationType.NavigationType_Previous:
            self.previous()


    def processDate(self, in_dateday, in_datemonth, in_dateyear):
        logger.info("Day {}, Month {}, Year {}".format(in_dateday, in_datemonth, in_dateyear))
        self.queue_event.put({'date':{'day':in_dateday, 'month':in_datemonth, 'year':in_dateyear}})

    def processTime(self, in_timehour, in_timeminute, in_timesecond):
        logger.info("Hour {}, Minute {}, Second {}".format(in_timehour, in_timeminute, in_timesecond))
        self.queue_event.put({'time':{'hour':in_timehour, 'minute':in_timeminute, 'second':in_timesecond}})
        

    def processSendBatteryStatus(self, in_sendbatterystatuspercentage):
        self.queue_event.put({'battery_status':in_sendbatterystatuspercentage})
        logger.info("Battery Status = {}".format(in_sendbatterystatuspercentage))

    def processSendProtocolVersion(self, in_sendprotocolversionmajor, in_sendprotocolversionminor):
        logger.info("FW Version: {}.{}".format(in_sendprotocolversionmajor, in_sendprotocolversionminor))

        # TODO: Update if needed...

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
        if self._selected_radio_bank is None:
            logger.warning("No bank selected...")
            return

        force_reload = False
        if position is not None:
            self._curr_position = position
        else:
            force_reload = True

        radios = self.lib["radio_banks"][self._selected_radio_bank]

        found_pos = self.find_closest_playable(self._curr_position, radios.keys())
        if found_pos is not None:
            if self._curr_played_position != found_pos or force_reload:
                ref_radio = radios[found_pos]
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

        self.queue_event.put({'tuner_position':self._curr_position})
        self.queue_event.put({'tuner_labels':{k:radios[k].name for k in radios}})

    def set_podcast(self, position=None):
        force_reload = False
        if position is not None:
            self._curr_position = position
        else:
            force_reload = True

        podcasts = self.lib['podcasts']

        found_pos = self.find_closest_playable(self._curr_position, podcasts.keys())
        if found_pos is not None:
            if self._curr_played_position != found_pos or force_reload:
                ref_pod = podcasts[found_pos]

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

        self.queue_event.put({'tuner_position':self._curr_position})
        self.queue_event.put({'tuner_labels':{k:podcasts[k].name for k in podcasts}})

    def set_next(self, **kwargs):
        if self.state == "podcast":
            self.core.playback.next()

        elif self.state == "radio":
            try:
                curr_index = self.lib["radio_banks"].keys().index(self._selected_radio_bank)
            except:
                curr_index = 0
            next_index = curr_index + 1
            if next_index == len(self.lib["radio_banks"]):
                next_index = 0

            self._selected_radio_bank = self.lib["radio_banks"].keys()[next_index]
            self.tuner()

    def set_previous(self, **kwargs):
        if self.state == "podcast":
            self.core.playback.previous()

        else:
            try:
                curr_index = self.lib["radio_banks"].keys().index(self._selected_radio_bank)
            except:
                curr_index = 0
            next_index = curr_index - 1
            if next_index < 0:
                next_index = len(self.lib["radio_banks"])-1

            self._selected_radio_bank = self.lib["radio_banks"].keys()[next_index]
            self.tuner()

    def turn_off_system(self, **kwargs):
        logger.warning("Turning Off")
        os.popen("sudo poweroff")