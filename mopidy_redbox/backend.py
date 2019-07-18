import logging

from mopidy import backend, exceptions, models

import pykka

logger = logging.getLogger(__name__)


class RedBoxBackend(pykka.ThreadingActor, backend.Backend):
    uri_schemes = [
        'redbox'
    ]

    def __init__(self, config, audio):
        super(RedBoxBackend, self).__init__()

        self.library = RedBoxLibraryProvider(backend=self)
        self.playback = RedBoxPlaybackProvider(audio=audio, backend=self)




class RedBoxLibraryProvider(backend.LibraryProvider):
    @property
    def root_directory(self):
        return models.Ref.directory(name='RedBox', uri="redbox:")


    def lookup(self, uri):
        logger.warning("lookup: {}".format(uri))
        return [models.Track(name=uri, uri=uri)]

    def browse(self, uri):
        if uri == 'redbox:':
            return [
                models.Ref.directory(name="RadioBankA", uri="redbox:bank_a"),
                models.Ref.directory(name="RadioBankB", uri="redbox:bank_b")
            ]
        elif uri == "redbox:bank_a":
            return [
                models.Ref.track(name="radio meuh", uri="redbox:bank_a:radio_meuh"),
                models.Ref.track(name="fip", uri="redbox:bank_a:fip")
            ]

        return []


class RedBoxPlaybackProvider(backend.PlaybackProvider):

    def translate_uri(self, uri):
        lut = {
            "redbox:bank_a:radio_meuh":"http://radiomeuh.ice.infomaniak.ch/radiomeuh-128.mp3",
            "redbox:bank_a:fip":"http://direct.fipradio.fr/live/fip-midfi.mp3"
        }
        return lut[uri]
