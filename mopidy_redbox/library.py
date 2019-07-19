import collections
import os
import mopidy
import logging
import unicodedata
import urllib2
import podcastparser
import threading

from mopidy import local
from mopidy.internal import storage as internal_storage


logger = logging.getLogger(__name__)

class Library(object):
    def __init__(self, json_file, podcast_timeout=5.0):
        self._json_file = json_file
        self._podcast_timeout = podcast_timeout
        self.load()

    def save(self):
        internal_storage.dump(self._json_file, self.data)

    def load(self):
        if not os.path.isfile(self._json_file):
            self.data = {
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
            }
            self.save()

        self.data = internal_storage.load(self._json_file)

        self.update_podcasts()



    def update_podcasts(self):
        def run():
            try:
                for podcast in self.data['podcasts']:
                    raw = urllib2.urlopen(podcast['feed_url'], timeout=self._podcast_timeout)
                    parsed = podcastparser.parse(podcast['feed_url'], raw)
                    episodes = parsed['episodes']

                    podcast['episodes'] = []

                    for episode in episodes:
                        title = episode['title']
                        media_url = episode['enclosures'][0]['url']

                        podcast['episodes'].append({"title":unicodedata.normalize('NFKD', title).encode('ascii','ignore'), "url":media_url})

                self.save()
                logger.info("Redbox Library: done downloading podcasts infos")
            
            except Exception as e:
                logger.error("RedBox: Can't retrieve podcast data: {}".format(str(e)))


        thr = threading.Thread(target=run)
        thr.start()