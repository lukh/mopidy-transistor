import logging
import os

import mopidy
from mopidy import backend, exceptions, models

from mopidy import local
from mopidy.internal import storage as internal_storage

import pykka

import urllib
import podcastparser

import mopidy_redbox
import library

logger = logging.getLogger(__name__)


class RedBoxBackend(pykka.ThreadingActor, backend.Backend):
    uri_schemes = [
        'redbox'
    ]

    def __init__(self, config, audio):
        super(RedBoxBackend, self).__init__()

        lib = library.Library(os.path.join(mopidy_redbox.Extension.get_data_dir(config), b'library.json.gz'))
        lib.load()

        self.library = RedBoxLibraryProvider(self, lib)
        self.playback = RedBoxPlaybackProvider(audio, self, lib)




class RedBoxLibraryProvider(backend.LibraryProvider):
    def __init__(self, backend, lib):
        super(RedBoxLibraryProvider, self).__init__(backend)
        self.lib = lib

    @property
    def root_directory(self):
        return models.Ref.directory(name='RedBox', uri="redbox:")

    def refresh(self, uri=None):
        self.lib.load()


    def lookup(self, uri):
        if not uri.startswith("redbox:"):
            return []

        split_uri = uri.split(":")

        if len(split_uri) == 4:
            if split_uri[1] == "radios":
                bank_radios = self.lib.data['radio_banks'][split_uri[2]]
                for rad in bank_radios:
                    if rad['name'] == split_uri[3]:
                        return [models.Track(name=rad['name'], uri=uri)]


            if split_uri[1] == "podcasts":
                for podcast in self.lib.data['podcasts']:
                    if split_uri[2] == podcast['name']:
                        for ep in podcast['episodes']:
                            if split_uri[3] == ep['title']:
                                return [models.Track(name=ep['title'], uri=uri)]



        return []

    def browse(self, uri):
        if not uri.startswith("redbox:"):
            return []

        split_uri = uri.split(":")

        # root
        if len(split_uri) == 2:
            if split_uri[1] == "":
                return [
                    models.Ref.directory(name="Radios", uri="redbox:radios"),
                    models.Ref.directory(name="Podcast", uri="redbox:podcasts")
                ]

            if split_uri[1] == "radios":
                return [
                    models.Ref.directory(name=bank, uri="redbox:radios:{}".format(bank)) for bank in self.lib.data["radio_banks"]
                ]

            if split_uri[1] == "podcasts":
                return [
                    models.Ref.directory(name=podcast['name'], uri="redbox:podcasts:{}".format(podcast['name'])) for podcast in self.lib.data["podcasts"]
                ]

        if len(split_uri) == 3:
            if split_uri[1] == "radios":
                return [
                    models.Ref.track(name=radio['name'], uri="redbox:radios:{}:{}".format(split_uri[2], radio['name'])) for radio in self.lib.data['radio_banks'][split_uri[2]]
                ]
            if split_uri[1] == "podcasts":
                for podcast in self.lib.data['podcasts']:
                    if split_uri[2] == podcast['name']:
                        return [
                            models.Ref.track(name=episode['title'], uri="redbox:podcasts:{}:{}".format(split_uri[2], episode['title'])) 
                                for episode in podcast['episodes']
                        ]
        return []


class RedBoxPlaybackProvider(backend.PlaybackProvider):
    def __init__(self, audio, backend, lib):
        super(RedBoxPlaybackProvider,  self).__init__(audio, backend)
        self.lib = lib

    def translate_uri(self, uri):
        if not uri.startswith("redbox:"):
            return ""

        split_uri = uri.split(":")

        if len(split_uri) == 4:
            if split_uri[1] == "radios":
                bank_radios = self.lib.data['radio_banks'][split_uri[2]]
                for rad in bank_radios:
                    if rad['name'] == split_uri[3]:
                        return rad['stream_url']

            if split_uri[1] == "podcasts":
                for podcast in self.lib.data['podcasts']:
                    if split_uri[2] == podcast['name']:
                        for ep in podcast['episodes']:
                            if split_uri[3] == ep['title']:
                                return ep['url']

        return ""
