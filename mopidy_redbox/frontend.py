import pykka
import logging

from mopidy import core
from mopidy.exceptions import FrontendError

logger = logging.getLogger(__name__)


class RedBoxFrontend(pykka.ThreadingActor, core.CoreListener):
    def __init__(self, config, core):
        super(RedBoxFrontend, self).__init__()

        self.core = core

    def on_start(self):
        logger.info('REDBOX FRont End Running')


    # def on_event(self, name, **data):
    #     logger.info('REDBOX:' + str(name) + ", " + str(data))