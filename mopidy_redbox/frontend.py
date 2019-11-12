import pykka
import logging
import serial
from threading import Thread
from queue import Queue

from mopidy import core
from mopidy.exceptions import FrontendError

import interface

logger = logging.getLogger(__name__)


class RedBoxFrontend(pykka.ThreadingActor, core.CoreListener):
    # used to push data to the event source (tuner, radios list, battery)
    queue_event = Queue()
    # used to communicate between front and web.
    queue_front = Queue()
    queue_web = Queue()

    def __init__(self, config, core):
        super(RedBoxFrontend, self).__init__()

        self.core = core
        self.config = config

    def on_start(self):
        logger.info('REDBOX Front End Running')

        self.interface = interface.SerialInterfaceListener(self.core, self.config, RedBoxFrontend.queue_event, RedBoxFrontend.queue_front, RedBoxFrontend.queue_web)
        self.interface.start()


    def on_stop(self):
        self.interface.stop = True
        self.interface.join()

    # def on_event(self, name, **data):
    #     logger.info('REDBOX:' + str(name) + ", " + str(data))