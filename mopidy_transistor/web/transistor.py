import os

from .basics import BaseHandler

import tornado.web

import mopidy_transistor
from mopidy_transistor import library


class RadioHandler(BaseHandler):
    def initialize(self, core, config):
        self.core = core
        self.lib = library.Library(
            os.path.join(
                mopidy_transistor.Extension.get_data_dir(config), "library.json.gz"
            ),
            podcast_timeout=config["transistor"]["podcasts_timeout"],
        )

    @tornado.web.authenticated
    def get(self, radio_bank=None):
        self.lib.load()
        radios = self.lib.data["radio_banks"]

        if radio_bank is None:
            if len(radios) > 0:
                radio_bank = list(radios.keys())[0]

        if radio_bank not in radios:
            radio_bank = None

        self.render(
            "site/radios.html",
            active_page="radios",
            radios=radios,
            radio_bank=radio_bank,
        )

    def post(self, *args, **kwargs):
        del_bank = self.get_argument("del_bank", None)
        if del_bank:
            if del_bank in self.lib.data["radio_banks"]:
                del self.lib.data["radio_banks"][del_bank]
                self.lib.save()
                self.core.library.refresh("transistor:")

        new_bank = self.get_argument("new_bank", None)
        if new_bank:
            if new_bank not in self.lib.data["radio_banks"]:
                self.lib.data["radio_banks"][new_bank] = []
                self.lib.save()
                self.core.library.refresh("transistor:")

        add_radio = self.get_argument("add_radio", None)
        if add_radio:
            if add_radio in self.lib.data["radio_banks"]:
                self.lib.data["radio_banks"][add_radio].append(
                    {
                        "name": self.get_argument("name"),
                        "position": int(self.get_argument("position")),
                        "stream_url": self.get_argument("url"),
                    }
                )
                self.lib.save()
                self.core.library.refresh("transistor:")

        del_radio_bank = self.get_argument("del_radio_bank", None)
        if del_radio_bank:
            del_radio_radio_index = int(self.get_argument("del_radio_radio", None))
            if del_radio_bank in self.lib.data["radio_banks"]:
                radios = self.lib.data["radio_banks"][del_radio_bank]
                if del_radio_radio_index < len(radios):
                    del radios[del_radio_radio_index]
                    self.lib.save()
                    self.core.library.refresh("transistor:")

        modify_radio_bank = self.get_argument("modify_radio_bank", None)
        if modify_radio_bank:
            id = int(self.get_argument("id", None))
            position = int(self.get_argument("position", None))
            name = self.get_argument("name", None)
            url = self.get_argument("url", None)
            if modify_radio_bank in self.lib.data["radio_banks"]:
                radios = self.lib.data["radio_banks"][modify_radio_bank]
                if id < len(radios):
                    radio = radios[id]

                    radio["name"] = name
                    radio["position"] = position
                    radio["stream_url"] = url

                    self.lib.save()
                    self.core.library.refresh("transistor:")

        self.redirect("radios")


class PodcastHandler(BaseHandler):
    def initialize(self, core, config):
        self.core = core
        self.lib = library.Library(
            os.path.join(
                mopidy_transistor.Extension.get_data_dir(config), "library.json.gz"
            ),
            podcast_timeout=config["transistor"]["podcasts_timeout"],
        )

    @tornado.web.authenticated
    def get(self):
        self.lib.load()
        podcasts = self.lib.data["podcasts"]

        self.render("site/podcasts.html", active_page="podcasts", podcasts=podcasts)

    def post(self, *args, **kwargs):
        podcasts = self.lib.data["podcasts"]

        del_podcast = self.get_argument("del_podcast", None)
        if del_podcast is not None:
            id = int(del_podcast)
            if id < podcasts:
                del podcasts[id]

                self.lib.save()
                self.core.library.refresh("transistor:")

        add_podcast = self.get_argument("add_podcast", None)
        if add_podcast is not None:
            podcasts.append(
                {
                    "name": self.get_argument("name"),
                    "position": int(self.get_argument("position")),
                    "feed_url": self.get_argument("url"),
                    "episodes": [],
                }
            )
            self.lib.save()
            self.core.library.refresh("transistor:")

        self.redirect("podcasts")
