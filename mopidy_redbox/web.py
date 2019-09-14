import os
import tornado.web
import mopidy_redbox
import library
from collections import OrderedDict
from ConfigParser import SafeConfigParser
import bcrypt

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class MainHandler(BaseHandler):
    def initialize(self):
        pass

    def get(self):
        self.render("site/index.html", active_page="index")

class AboutHandler(BaseHandler):
    def initialize(self):
        pass

    def get(self):
        self.render("site/about.html", active_page="about")

class AlarmsHandler(BaseHandler):
    def initialize(self):
        pass

    def get(self):
        self.render("site/alarms.html", active_page="alarms")

class SettingsHandler(BaseHandler):
    def initialize(self, config):
        self.config_file = config['redbox']['config_file']

    @tornado.web.authenticated
    def get(self):
        parser = SafeConfigParser()
        parser.read(self.config_file)

        config = OrderedDict()
        for section in parser.sections():
            if len(parser.items(section)) != 0:
                config[section] = OrderedDict()
                for name, value in parser.items(section):
                    if section == "redbox" and name == "passwd":
                        config[section][name] = ""
                    else:
                        config[section][name] = value

        self.render('site/settings.html', active_page="settings", config=config)

    def post(self, *args, **kwargs):
        section = self.get_argument("section")
        # all internal settings
        parser = SafeConfigParser()
        parser.read(self.config_file)

        for name in parser.options(section):
            if section == "redbox" and name == "passwd":
                if self.get_argument(name) != "":
                    hashed = bcrypt.hashpw(str(self.get_argument(name)), bcrypt.gensalt())
                    parser.set(section, name, hashed)

            else:
                parser.set(section, name, self.get_argument(name))


        with open(self.config_file, 'w') as fp:
            parser.write(fp)

        self.redirect('settings')



class WifiHandler(BaseHandler):
    def initialize(self):
        pass

    @tornado.web.authenticated
    def get(self):
        ssids = []
        self.render("site/wifi.html", active_page="wifi", ssids=ssids, valid_ssid=None)


    def post(self):
        ssids = self.get_argument('ssids', "")
        ssid_other = self.get_argument('ssid_other', "")
        passwd = self.get_argument('passwd')

        if ssids == "" and ssid_other == "":
            self.render("site/wifi.html", active_page="wifi", valid_ssid=None, ssids=None)
            return

        ssid = ssid_other if ssid_other != "" else ssids
        self.render("site/wifi.html", active_page="wifi", valid_ssid=ssid, ssids=None)

        # os.popen('sudo redbox_wifi connect {} {}'.format(ssid, passwd))
        print('sudo redbox_wifi connect {} {}'.format(ssid, passwd))


class LoginHandler(BaseHandler):
    def initialize(self, config):
        self._user = config['redbox']['user']
        self._hashed_passwd = config['redbox']['passwd']

    def get(self):
        if self._user == None and self._hashed_passwd == None:
            self.set_secure_cookie("user", "none")
            self.redirect(self.get_argument('next', '/'))
        else:
            self.render("site/login.html", active_page="login", next=self.get_argument('next', '/'), error_msg=None)

    def post(self):
        user = self.get_argument('user')
        raw_passwd = str(self.get_argument('passwd'))

        if (self._user is None and self._hashed_passwd is None) or (user == self._user and bcrypt.checkpw(raw_passwd, str(self._hashed_passwd))):
            self.set_secure_cookie("user", user)
            self.redirect(self.get_argument('next', '/'))

        else:
            self.render("site/login.html", active_page="login", next=self.get_argument('next', '/'), error_msg="Can't Log In...")

class BrowseHandler(BaseHandler):
    def initialize(self):
        pass

    def get(self):
        self.render("site/browse.html", active_page="browse")


class RadioHandler(BaseHandler):
    def initialize(self, core, config):
        self.core = core
        self.lib = library.Library(os.path.join(mopidy_redbox.Extension.get_data_dir(config), b'library.json.gz'), podcast_timeout=config['redbox']['podcasts_timeout'])

    @tornado.web.authenticated
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




class PodcastHandler(BaseHandler):
    def initialize(self, core, config):
        self.core = core
        self.lib = library.Library(os.path.join(mopidy_redbox.Extension.get_data_dir(config), b'library.json.gz'), podcast_timeout=config['redbox']['podcasts_timeout'])

    @tornado.web.authenticated
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
