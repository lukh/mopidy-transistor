import os
import tornado.web
import mopidy_redbox
import library
from collections import OrderedDict
from ConfigParser import SafeConfigParser

import wifi

class MainHandler(tornado.web.RequestHandler):
    def initialize(self):
        pass

    def get(self):
        self.render("site/index.html", active_page="index")

class AboutHandler(tornado.web.RequestHandler):
    def initialize(self):
        pass

    def get(self):
        self.render("site/about.html", active_page="about")

class SettingsHandler(tornado.web.RequestHandler):
    def initialize(self, config):
        self.config_file = config['redbox']['config_file']

    def get(self):
        parser = SafeConfigParser()
        parser.read(self.config_file)

        config = OrderedDict()
        for section in parser.sections():
            if len(parser.items(section)) != 0:
                config[section] = OrderedDict()
                for name, value in parser.items(section):
                    config[section][name] = value

        ssids = wifi.scan_networks("wlan0")

        self.render('site/settings.html', active_page="settings", config=config, ssids=ssids)

    def post(self, *args, **kwargs):
        section = self.get_argument("section", None)
        if section is not None:
            # all internal settings
            if section != "wifi":
                parser = SafeConfigParser()
                parser.read(self.config_file)

                for name in parser.options(section):
                    parser.set(section, name, self.get_argument(name))


                with open(self.config_file, 'w') as fp:
                    parser.write(fp)

                self.redirect('settings')

            # wifi
            else:
                ssids = self.get_argument('ssids', "")
                ssid_other = self.get_argument('ssid_other', "")
                passwd = self.get_argument('passwd')

                if ssids == "" and ssid_other == "":
                    self.render("site/wifi.html", active_page="", ssid=None)
                    return

                ssid = ssid_other if ssid_other != "" else ssids
                self.render("site/wifi.html", active_page="", ssid=ssid)

                # os.popen('sudo redbox_wifi connect {} {}'.format(ssid, passwd))
                print('sudo redbox_wifi connect {} {}'.format(ssid, passwd))





class BrowseHandler(tornado.web.RequestHandler):
    def initialize(self):
        pass

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

        del_radio_bank = self.get_argument('del_radio_bank', None)
        if del_radio_bank:
            del_radio_radio_index = int(self.get_argument('del_radio_radio', None))
            if del_radio_bank in self.lib.data['radio_banks']:
                radios = self.lib.data['radio_banks'][del_radio_bank]
                if(del_radio_radio_index < len(radios)):
                    del radios[del_radio_radio_index]
                    self.lib.save()
                    self.core.library.refresh('redbox:')


        modify_radio_bank = self.get_argument('modify_radio_bank', None)
        if modify_radio_bank:
            id = int(self.get_argument('id', None))
            position = int(self.get_argument('position', None))
            name = self.get_argument('name', None)
            url = self.get_argument('url', None)
            if modify_radio_bank in self.lib.data['radio_banks']:
                radios = self.lib.data['radio_banks'][modify_radio_bank]
                if(id < len(radios)):
                    radio = radios[id]

                    radio['name'] = name
                    radio['position'] = position
                    radio['stream_url'] = url

                    self.lib.save()
                    self.core.library.refresh('redbox:')

        self.redirect('radios')




class PodcastHandler(tornado.web.RequestHandler):
    def initialize(self, core, config):
        self.core = core
        self.lib = library.Library(os.path.join(mopidy_redbox.Extension.get_data_dir(config), b'library.json.gz'), podcast_timeout=config['redbox']['podcasts_timeout'])

    def get(self):
        self.lib.load()
        podcasts = self.lib.data['podcasts']
        
        self.render("site/podcasts.html", active_page="podcasts", podcasts=podcasts)

    def post(self, *args, **kwargs):
        podcasts = self.lib.data['podcasts']

        del_podcast = self.get_argument("del_podcast", None)
        if del_podcast is not None:
            id = int(del_podcast)
            if(id < podcasts):
                del podcasts[id]

                self.lib.save()
                self.core.library.refresh('redbox:')

        add_podcast = self.get_argument("add_podcast", None)
        if add_podcast is not None:
            podcasts.append(
                {
                    "name":self.get_argument("name"),
                    "position":int(self.get_argument("position")),
                    "feed_url":self.get_argument("url"),
                    "episodes":[],
                }
            )
            self.lib.save()
            self.core.library.refresh('redbox:')

        self.redirect('podcasts')
