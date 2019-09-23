from ConfigParser import SafeConfigParser
from collections import OrderedDict

from basics import BaseHandler

import bcrypt

import tornado.web

from settings_conf import settings_conf


class SettingsHandler(BaseHandler):
    def initialize(self, config):
        self.config = config
        self.config_file = config['redbox']['config_file']

    @tornado.web.authenticated
    def get(self):
        config = OrderedDict()
        for sc in settings_conf:
            section = sc[0]
            config[section] = OrderedDict()
            for name in sc[1]:
                if section == "redbox" and name == "passwd":
                    config[section]['new_passwd'] = ""
                    config[section]['repeat_passwd'] = ""
                    config[section]['old_passwd'] = ""
                else:
                    config[section][name] = self.config[section][name]
                    if config[section][name] is None:
                        config[section][name] = ""

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

        for sc in settings_conf:
            if sc[0] == section:
                break
        else:
            self.redirect('settings')
            return

        for name in sc[1]:
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
                if self.get_argument(name) != "":
                    parser.set(section, name, self.get_argument(name))

        with open(self.config_file, 'w') as fp:
            parser.write(fp)

        self.redirect('settings?passwd_updated={}'.format(passwd_updated))



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