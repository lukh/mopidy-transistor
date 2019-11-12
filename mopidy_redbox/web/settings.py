from ConfigParser import SafeConfigParser
from collections import OrderedDict

from basics import BaseHandler

import bcrypt

import tornado.web
import tornado.websocket

from settings_conf import settings_conf


class SettingsHandler(BaseHandler):
    def initialize(self, config):
        self.config = config
        self.config_file = config['redbox']['config_file']

    @tornado.web.authenticated
    def get(self):
        config = OrderedDict()
        for section in settings_conf:
            config[section] = OrderedDict()
            for name, param_type in settings_conf[section]:
                if section == "redbox" and name == "passwd":
                    config[section]['new_passwd'] = ["", "password"]
                    config[section]['repeat_passwd'] = ["", "password"]
                    config[section]['old_passwd'] = ["", "password"]
                else:
                    config[section][name] = [
                        self.config[section][name],
                        param_type]

                    if config[section][name][0] is None:
                        config[section][name][0] = ""

        passwd_updated = self.get_argument("passwd_updated", "0")
        lut_pu = {
            "0": None,
            "1": "Password updated successfully",
            "2": "Error while updating password"
        }

        self.render(
            'site/settings.html',
            active_page="settings",
            config=config,
            warning_msg=lut_pu.get(passwd_updated, None)
        )

    def post(self, *args, **kwargs):
        section = self.get_argument("section")
        # all internal settings
        parser = SafeConfigParser()
        parser.read(self.config_file)

        passwd_updated = 0

        for name, param_type in settings_conf[section]:
            if section == "redbox" and name == "passwd":
                new_pass = self.get_argument('new_passwd')
                rep_passwd = self.get_argument('repeat_passwd')
                old_passwd = self.get_argument('old_passwd')

                if new_pass == "":
                    pass

                elif new_pass != "":
                    if self.config['redbox']['passwd'] is None or \
                            new_pass == rep_passwd and \
                            bcrypt.checkpw(
                                str(old_passwd),
                                str(self.config['redbox']['passwd'])):

                        hashed = bcrypt.hashpw(str(new_pass), bcrypt.gensalt())
                        parser.set(section, name, hashed)
                        passwd_updated = 1  # valid
                    else:
                        passwd_updated = 2  # error

            else:
                value = self.get_argument(name)
                if value == "":
                    value = None
                else:
                    if param_type == "int":
                        value = int(value)
                    elif param_type == "bool":
                        value = value in ['true', 'True']
                    elif param_type == "tuple":
                        value = value.replace(';', '\n')

                parser.set(section, name, value)

        with open(self.config_file, 'w') as fp:
            parser.write(fp)

        self.redirect('settings?passwd_updated={}'.format(passwd_updated))


class WifiHandler(BaseHandler):
    def initialize(self):
        pass

    @tornado.web.authenticated
    def get(self):
        ssids = []
        self.render(
            "site/wifi.html",
            active_page="wifi",
            ssids=ssids,
            valid_ssid=None)

    def post(self):
        ssids = self.get_argument('ssids', "")
        ssid_other = self.get_argument('ssid_other', "")
        passwd = self.get_argument('passwd')

        if ssids == "" and ssid_other == "":
            self.render(
                "site/wifi.html",
                active_page="wifi",
                valid_ssid=None,
                ssids=None)
            return

        ssid = ssid_other if ssid_other != "" else ssids
        self.render(
            "site/wifi.html",
            active_page="wifi",
            valid_ssid=ssid,
            ssids=None)

        # os.popen('sudo redbox_wifi connect {} {}'.format(ssid, passwd))
        print('sudo redbox_wifi connect {} {}'.format(ssid, passwd))

class CalibrationHandler(BaseHandler):
    def initialize(self):
        pass

    def get(self):
        self.render("site/calibration.html", active_page="calibration")

class CalibrationWebSocketHandler(tornado.websocket.WebSocketHandler):
    def initialize(self, queue_front, queue_web):
        self._queue_front = queue_front
        self._queue_web = queue_web

    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        self.write_message(u"You said: " + message)

    def on_close(self):
        print("WebSocket closed")
