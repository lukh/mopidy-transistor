import os
import tornado.web
import mopidy_redbox
import library

class MainHandler(tornado.web.RequestHandler):
    def initialize(self):
        pass

    def get(self):
        self.render("site/index.html", active_page="index")
        

class BrowseHandler(tornado.web.RequestHandler):
    def initialize(self, core):
        self.core = core

    def get(self):
        self.render("site/browse.html", active_page="browse")


class RadioHandler(tornado.web.RequestHandler):
    def initialize(self, core, config):
        self.core = core
        self.lib = library.Library(os.path.join(mopidy_redbox.Extension.get_data_dir(config), b'library.json.gz'), podcast_timeout=config['redbox']['podcasts_timeout'])

    def get(self, radio_bank=None):
        self.lib.load()
        radios = self.lib.data['radio_banks']
        
        if radio_bank is None:
            if len(radios) > 0:
                radio_bank = radios.keys()[0]

        if radio_bank not in radios:
            radio_bank = None

        self.render("site/radios.html", active_page="radios", radios=radios, radio_bank=radio_bank)

    def post(self, *args, **kwargs):
        del_bank = self.get_argument('del_bank', None)
        if del_bank:
            if del_bank in self.lib.data['radio_banks']:
                del self.lib.data['radio_banks'][del_bank]
                self.lib.save()
                self.core.library.refresh('redbox:')

        new_bank = self.get_argument('new_bank', None)
        if new_bank:
            if new_bank not in self.lib.data['radio_banks']:
                self.lib.data['radio_banks'][new_bank] = []
                self.lib.save()
                self.core.library.refresh('redbox:')


        add_radio = self.get_argument('add_radio', None)
        if add_radio:
            if add_radio in self.lib.data['radio_banks']:
                self.lib.data['radio_banks'][add_radio].append({
                    "name":self.get_argument("name"),
                    "position":int(self.get_argument("position")),
                    "stream_url":self.get_argument("url"),
                })
                self.lib.save()
                self.core.library.refresh('redbox:')

        self.redirect('radios')