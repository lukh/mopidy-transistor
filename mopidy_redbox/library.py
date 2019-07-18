import collections
import os
import mopidy

from mopidy import local
from mopidy.internal import storage as internal_storage

class Library(object):
    def __init__(self, json_file):
        self._json_file = json_file


    def close(self):
        internal_storage.dump(self._json_file, self.data)

    def load(self):
        if not os.path.isfile(self._json_file):
            internal_storage.dump(self._json_file, {
                'version': mopidy.__version__,
                'radio_banks': {
                    "AM":[
                        {"name":"FIP", "stream_url":"http://direct.fipradio.fr/live/fip-midfi.mp3"},
                        {"name":"Meeeuh", "stream_url":"http://radiomeuh.ice.infomaniak.ch/radiomeuh-128.mp3"}
                    ],
                    "FM":[]
                }
            })

        self.data = internal_storage.load(self._json_file)