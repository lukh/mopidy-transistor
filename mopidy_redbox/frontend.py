import pykka
import logging
import serial
from threading import Thread

from mopidy import core
from mopidy.exceptions import FrontendError

import interface

logger = logging.getLogger(__name__)


class RedBoxFrontend(pykka.ThreadingActor, core.CoreListener):
    def __init__(self, config, core):
        super(RedBoxFrontend, self).__init__()

        self.core = core
        self.config = config

    def on_start(self):
        logger.info('REDBOX FRont End Running')

        self.interface = interface.SerialInterfaceListener(self.config)
        self.interface.start()


    def on_stop(self):
        self.interface.stop = True
        self.interface.join()

    # def on_event(self, name, **data):
    #     logger.info('REDBOX:' + str(name) + ", " + str(data))