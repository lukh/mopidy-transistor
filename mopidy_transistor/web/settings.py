from configparser import SafeConfigParser
from collections import OrderedDict
import datetime
import os
import json
from enum import Enum

import bcrypt
import subprocess

import tornado.web
import tornado.websocket
import tornado.gen
import tornado.ioloop

from transitions import Machine, State

from .basics import BaseHandler
from .settings_conf import settings_conf

import mopidy_transistor

from mopidy_transistor.protocol.TransistorMsg import TransistorMsg


class SettingsHandler(BaseHandler):
    def initialize(self, config):
        self.config = config
        self.config_file = config["transistor"]["config_file"]

    @tornado.web.authenticated
    def get(self):
        config = OrderedDict()
        for section in settings_conf:
            config[section] = OrderedDict()
            for name, param_type in settings_conf[section]:
                if section == "transistor" and name == "passwd":
                    config[section]["new_passwd"] = ["", "password"]
                    config[section]["repeat_passwd"] = ["", "password"]
                    config[section]["old_passwd"] = ["", "password"]
                else:
                    config[section][name] = [
                        self.config.get(section, {}).get(name, None),
                        param_type,
                    ]

                    if config[section][name][0] is None:
                        config[section][name][0] = ""

        passwd_updated = self.get_argument("passwd_updated", "0")
        lut_pu = {
            "0": None,
            "1": "Password updated successfully",
            "2": "Error while updating password",
        }

        uploaded_data_status = self.get_argument("uploaded_data_status", None)

        self.render(
            "site/settings.html",
            active_page="settings",
            config=config,
            active_section="transistor",
            warning_msg=lut_pu.get(passwd_updated, None),
            uploaded_data_status=uploaded_data_status
        )

    def post(self, *args, **kwargs):
        section = self.get_argument("section")
        # all internal settings
        parser = SafeConfigParser()
        parser.read(self.config_file)

        passwd_updated = 0

        for name, param_type in settings_conf[section]:
            if section == "transistor" and name == "passwd":
                new_pass = self.get_argument("new_passwd")
                rep_passwd = self.get_argument("repeat_passwd")
                old_passwd = self.get_argument("old_passwd")

                if new_pass == "":
                    pass

                elif new_pass != "":
                    if (
                        self.config["transistor"]["passwd"] is None
                        or new_pass == rep_passwd
                        and bcrypt.checkpw(
                            str(old_passwd),
                            str(self.config["transistor"]["passwd"]),
                        )
                    ):

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
                        value = value in ["true", "True"]
                    elif param_type == "tuple":
                        value = value.replace(";", "\n")

                parser.set(section, name, value)

        with open(self.config_file, "w") as fp:
            parser.write(fp)

        self.redirect("settings?passwd_updated={}".format(passwd_updated))


class UploadLibraryHandler(BaseHandler):
    def initialize(self, config):
        self.config = config

    def post(self):
        uploaded_data_status = "Can't upload data file"
        try:
            file1 = self.request.files["file_backup_upload"][0]
            original_fname = file1["filename"]

            if original_fname == "library.json.gz":
                output_file_path = os.path.join(
                    mopidy_transistor.Extension.get_data_dir(self.config),
                    "library.json.gz",
                )
                output_file = open(output_file_path, "wb")
                output_file.write(file1["body"])

                uploaded_data_status = "The file has been uploaded successfully"

        except KeyError:
            pass

        self.redirect("settings?uploaded_data_status={}".format(uploaded_data_status))


class WifiHandler(BaseHandler):
    def initialize(self):
        pass

    @tornado.web.authenticated
    def get(self):
        # scan availables networks
        pid = subprocess.Popen(
            "yawap --list", stdout=subprocess.PIPE, stderr=None, shell=True
        )
        output, _ = pid.communicate()
        output = str(output, "utf-8", "ignore").strip("\n")
        ssids = output.split(";")

        # scan saved networks
        pid = subprocess.Popen(
            "yawap --list-saved",
            stdout=subprocess.PIPE,
            stderr=None,
            shell=True,
        )
        output, _ = pid.communicate()
        output = str(output, "utf-8", "ignore").strip("\n")
        saved_ssids = output.split(";")

        self.render(
            "site/wifi.html",
            active_page="wifi",
            ssids=ssids,
            valid_ssid=None,
            saved_ssids=saved_ssids,
        )

    def post(self):
        ssids = self.get_argument("ssids", "")
        ssid_other = self.get_argument("ssid_other", "")
        passwd = self.get_argument("passwd", "")

        del_ssid = self.get_argument("del_ssid", "")
        if del_ssid != "":
            subprocess.Popen("yawap --delete {}".format(del_ssid), shell=True)
            self.redirect("wifi")

        else:
            if (ssids == "" and ssid_other == "") or passwd == "":
                self.render(
                    "site/wifi.html",
                    active_page="wifi",
                    valid_ssid=None,
                    ssids=None,
                    saved_ssids=None,
                )
                return

            else:
                ssid = ssid_other if ssid_other != "" else ssids
                self.render(
                    "site/wifi.html",
                    active_page="wifi",
                    valid_ssid=ssid,
                    ssids=None,
                    saved_ssids=None,
                )

                subprocess.Popen(
                    "yawap --add {} {}".format(ssid, passwd), shell=True
                )


class UpdateWifiCountryCodehandler(BaseHandler):
    def post(self):
        country = self.get_argument("country", None)
        if country is not None:
            subprocess.Popen(
                "yawap --set-wpa-supplicant-conf country {}".format(country),
                shell=True,
            )

        self.redirect("wifi")


class UpdateHandler(BaseHandler):
    def initialize(self):
        pass

    @tornado.web.authenticated
    def get(self):
        self.render("site/update.html", active_page="update")


class UpdateWebSocketHandler(tornado.websocket.WebSocketHandler):
    STATE = "IDLE"

    def initialize(self):
        pass

    @tornado.gen.coroutine
    def on_message(self, msg):
        def execute(cmd):
            pid = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            while pid.poll() is None:
                line = pid.stdout.readline()
                if line is not None:
                    yield self.write_message(line)

        if self.STATE == "IDLE":
            if msg == "update_system":
                self.STATE = "BUSY"
                self.write_message("Starting System Update...")

                execute("sudo apt-get update")
                execute("sudo apt-get upgrade")

                self.STATE = "DONE"  # need a refresh of the webpage to re execute an update

            elif msg == "update_mopidy":
                self.STATE = "BUSY"
                self.write_message("Starting Mopidy Update...")

                execute("sudo apt-get update")
                # execute("sudo apt-get upgrade python-mopidy")

                self.STATE = "DONE"  # need a refresh of the webpage to re execute an update


class CalibrationHandler(BaseHandler):
    def initialize(self):
        self.potentiometers = {
          p.value:p.name.split("_")[1] for p in TransistorMsg.CalibratePotentiometer
        }

    def get(self):
        self.render("site/calibration.html", active_page="calibration", potentiometers=self.potentiometers)


class CalibrationWebSocketHandler(tornado.websocket.WebSocketHandler):
    class CalibrationPhase(Enum):
        Low = "Low"
        High = "High"

    def initialize(self, core):
        self.core = core
        Machine(
            model=self,
            states=[
                {"name":"idle"},
                {"name":"turn"},
                {"name":"start_calibrate"},
                {"name":"stop_calibrate"},
                {"name":"save"}
            ],
            transitions=[
                {
                    "trigger": "start",
                    "source": "idle",
                    "dest": "turn",
                },
                {
                    "trigger": "next_step",
                    "source": "turn",
                    "dest": "start_calibrate",
                },
                {
                    "trigger": "timeout",
                    "source": "start_calibrate",
                    "dest": "stop_calibrate",
                },
                {
                    "trigger": "timeout",
                    "source": "stop_calibrate",
                    "dest": "turn",
                    "before":"increment_phase",
                    "conditions":"is_not_finished"
                },
                {
                    "trigger": "timeout",
                    "source": "stop_calibrate",
                    "dest": "save",
                    "before":"increment_phase",
                    "conditions":"is_finished"
                },
                {
                    "trigger":"timeout", 
                    "source": "save", 
                    "dest": "idle"
                },
            ],
            initial="idle",
            ignore_invalid_triggers=True,
        )

        self.potentiometer = None
        self.phase = self.CalibrationPhase.Low

    def increment_phase(self):
        self.phase = self.CalibrationPhase.High

    def is_finished(self):
        return self.phase == self.CalibrationPhase.High

    def is_not_finished(self):
        return not self.is_finished()

    def on_enter_idle(self):
        self.phase = self.CalibrationPhase.Low
        self.write_message(u"Done !")

    def on_enter_turn(self, potentiometer=None):
        if isinstance(potentiometer, TransistorMsg.CalibratePotentiometer):
            self.potentiometer = potentiometer
        self.write_message(f"Turn {self.potentiometer.name.split('_')[1]} to {self.phase.value} and press Next Step button")

    def on_enter_start_calibrate(self):
        self.write_message(f"Start {self.potentiometer.name.split('_')[1]} : {self.phase.value} Calibration, Wait...")
        self.wait(2)
        # self.core.transistor.process_websocket_message({"cmd": None})
        
    def on_enter_stop_calibrate(self):
        self.write_message(f"Saving {self.potentiometer.name.split('_')[1]} : {self.phase.value}")
        # self.core.transistor.process_websocket_message({"cmd": None})
        self.wait(0.5)

    def on_enter_save(self):
        self.write_message(u"Saving...")
        # self.core.transistor.process_websocket_message({"cmd": self.state})
        self.wait(0.5)
        
    def wait(self, seconds):
        tornado.ioloop.IOLoop.instance().add_timeout(
            datetime.timedelta(seconds=seconds), self.timeout
        )

    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        message = json.loads(message)
        cmd = message.get("cmd", "")

        pot_id = TransistorMsg.CalibratePotentiometer(int(message.get("pot-id", 0)))

        if cmd == "start":
            self.start(potentiometer=pot_id)

        if cmd == "next_step":
            self.next_step()


    def on_close(self):
        print("WebSocket closed")



