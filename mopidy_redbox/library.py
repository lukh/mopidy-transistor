import collections
import os
import mopidy
import logging

from mopidy import local
from mopidy.internal import storage as internal_storage

import urllib
import podcastparser
import threading


logger = logging.getLogger(__name__)

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
                },
                "podcasts":[
                    {"name":"TEDx", "feed_url":"http://www.npr.org/rss/podcast.php?id=510298", "episodes":[]},
                    {"name":"Revolt", "feed_url":"http://wordsmith.podomatic.com/rss2.xml", "episodes":[]},
                ]
            })

        self.data = internal_storage.load(self._json_file)

        self.update_podcasts()



    def update_podcasts(self):
        def run():
            for podcast in self.data['podcasts']:
                parsed = podcastparser.parse(podcast['feed_url'], urllib.urlopen(podcast['feed_url']))
                episodes = parsed['episodes']

                podcast['episodes'] = []

                for episode in episodes:
                    title = episode['title']
                    media_url = episode['enclosures'][0]['url']

                    podcast['episodes'].append({"title":title, "url":media_url})

            logger.info("Redbox Library: done downloading podcasts infos")

        thr = threading.Thread(target=run)
        thr.start()