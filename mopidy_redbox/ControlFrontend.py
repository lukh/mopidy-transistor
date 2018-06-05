import pykka

from mopidy import core


class ControlFrontend(pykka.ThreadingActor, core.CoreListener):
    """
        Handle the input from the Arduino via serial for changing the playlist
    """
    def __init__(self, config, core):
        super(ControlFrontend, self).__init__()
        self.core = core

    # Your frontend implementation