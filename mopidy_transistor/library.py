import mopidy
import logging
from urllib.request import urlopen
from pathlib import Path
import podcastparser
import threading

from mopidy.internal import storage as internal_storage


logger = logging.getLogger(__name__)


class Library(object):
    def __init__(self, json_file, podcast_timeout=5.0):
        self._json_file = Path(json_file)
        self._podcast_timeout = podcast_timeout
        self.load()

    def save(self):
        internal_storage.dump(self._json_file, self.data)

    def load(self):
        if not self._json_file.is_file():
            self.data = {
                "version": mopidy.__version__,
                "radio_banks": {
                    "AM": [
                        {
                            "name": "FIP",
                            "stream_url": "http://direct.fipradio.fr/live/fip-midfi.mp3",
                            "position": 64,
                        },
                        {
                            "name": "Meeeuh",
                            "stream_url": "http://radiomeuh.ice.infomaniak.ch/radiomeuh-128.mp3",
                            "position": 32,
                        },
                    ],
                    "FM": [
                        {
                            "name": "Inter",
                            "stream_url": "http://direct.franceinter.fr/live/franceinter-midfi.mp3",
                            "position": 32,
                        },
                        {
                            "name": "Culture",
                            "stream_url": "http://direct.franceculture.fr/live/franceculture-midfi.mp3",
                            "position": 64,
                        },
                    ],
                },
                "podcasts": [
                    {
                        "name": "TEDx",
                        "feed_url": "http://www.npr.org/rss/podcast.php?id=510298",
                        "episodes": [],
                        "position": 64,
                    },
                    {
                        "name": "Revolt",
                        "feed_url": "http://wordsmith.podomatic.com/rss2.xml",
                        "episodes": [],
                        "position": 32,
                    },
                    {
                        "name": "Neo Geo",
                        "feed_url": "http://feeds.feedburner.com/NeoGeoNova",
                        "position": 10,
                    },
                    {
                        "name": "Juke Box",
                        "feed_url": "http://radiofrance-podcast.net/podcast09/rss_16999.xml",
                        "position": 20,
                    },
                ],
            }
            self.save()

        self.data = internal_storage.load(self._json_file)

    def update_podcasts(self):
        def run():
            try:
                for podcast in self.data["podcasts"]:
                    raw = urlopen(podcast["feed_url"], timeout=self._podcast_timeout)
                    parsed = podcastparser.parse(podcast["feed_url"], raw)
                    episodes = parsed["episodes"]

                    podcast["episodes"] = []

                    for episode in episodes:
                        title = episode["title"]
                        media_url = episode["enclosures"][0]["url"]

                        # podcast['episodes'].append({"title":unicodedata.normalize('NFKD', title).encode('ascii','ignore'), "url":media_url})
                        podcast["episodes"].append({"title": title, "url": media_url})

                self.save()
                logger.info("Transistor Library: done downloading podcasts infos")

            except Exception as e:
                logger.error(
                    "Transistor: Can't retrieve podcast data: {}".format(str(e))
                )

        thr = threading.Thread(target=run)
        thr.start()
