from configparser import SafeConfigParser
from collections import OrderedDict
from threading import Timer

import bcrypt
import subprocess

import tornado.web
import tornado.websocket
import tornado.gen

from transitions import Machine, State

from .basics import BaseHandler
from .settings_conf import settings_conf


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

        self.render(
            "site/settings.html",
            active_page="settings",
            config=config,
            active_section="transistor",
            warning_msg=lut_pu.get(passwd_updated, None),
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
                            str(old_passwd), str(self.config["transistor"]["passwd"])
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


class WifiHandler(BaseHandler):
    def initialize(self):
        pass

    @tornado.web.authenticated
    def get(self):
        pid = subprocess.Popen(
            "yawap --list", stdout=subprocess.PIPE, stderr=None, shell=True
        )
        output, _ = pid.communicate()
        output = str(output, "utf-8", "ignore").strip("\n")
        ssids = output.split(";")

        self.render("site/wifi.html", active_page="wifi", ssids=ssids, valid_ssid=None)

    def post(self):
        ssids = self.get_argument("ssids", "")
        ssid_other = self.get_argument("ssid_other", "")
        passwd = self.get_argument("passwd")

        if ssids == "" and ssid_other == "":
            self.render(
                "site/wifi.html", active_page="wifi", valid_ssid=None, ssids=None
            )
            return

        ssid = ssid_other if ssid_other != "" else ssids
        self.render("site/wifi.html", active_page="wifi", valid_ssid=ssid, ssids=None)

        subprocess.Popen("yawap --add {} {}".format(ssid, passwd), shell=True)


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

                self.STATE = (
                    "DONE"  # need a refresh of the webpage to re execute an update
                )

            elif msg == "update_mopidy":
                self.STATE = "BUSY"
                self.write_message("Starting Mopidy Update...")

                execute("sudo apt-get update")
                # execute("sudo apt-get upgrade python-mopidy")

                self.STATE = (
                    "DONE"  # need a refresh of the webpage to re execute an update
                )


class CalibrationHandler(BaseHandler):
    def initialize(self):
        pass

    def get(self):
        self.render("site/calibration.html", active_page="calibration")


class CalibrationWebSocketHandler(tornado.websocket.WebSocketHandler):
    def initialize(self, queue_front, queue_web):
        self._queue_front = queue_front
        self._queue_web = queue_web

        Machine(
            model=self,
            states=[
                State("idle", on_enter=["handle_done"]),
                State("turn_volume_low", on_enter=["handle_turn_volume_low"]),
                State(
                    "start_calibrate_volume_low",
                    on_enter=["handle_start_calibrate_volume_low"],
                ),
                State(
                    "save_calibrate_volume_low",
                    on_enter=["handle_save_calibrate_volume_low"],
                ),
                State("turn_volume_high", on_enter=["handle_turn_volume_high"]),
                State(
                    "start_calibrate_volume_high",
                    on_enter=["handle_start_calibrate_volume_high"],
                ),
                State(
                    "save_calibrate_volume_high",
                    on_enter=["handle_save_calibrate_volume_high"],
                ),
                State("turn_tuner_low", on_enter=["handle_turn_tuner_low"]),
                State(
                    "start_calibrate_tuner_low",
                    on_enter=["handle_start_calibrate_tuner_low"],
                ),
                State(
                    "save_calibrate_tuner_low",
                    on_enter=["handle_save_calibrate_tuner_low"],
                ),
                State("turn_tuner_high", on_enter=["handle_turn_tuner_high"]),
                State(
                    "start_calibrate_tuner_high",
                    on_enter=["handle_start_calibrate_tuner_high"],
                ),
                State(
                    "save_calibrate_tuner_high",
                    on_enter=["handle_save_calibrate_tuner_high"],
                ),
                State("save", on_enter=["handle_save"]),
            ],
            transitions=[
                {"trigger": "next_step", "source": "idle", "dest": "turn_volume_low"},
                {
                    "trigger": "next_step",
                    "source": "turn_volume_low",
                    "dest": "start_calibrate_volume_low",
                },
                {
                    "trigger": "timeout",
                    "source": "start_calibrate_volume_low",
                    "dest": "save_calibrate_volume_low",
                },
                {
                    "trigger": "timeout",
                    "source": "save_calibrate_volume_low",
                    "dest": "turn_volume_high",
                },
                {
                    "trigger": "next_step",
                    "source": "turn_volume_high",
                    "dest": "start_calibrate_volume_high",
                },
                {
                    "trigger": "timeout",
                    "source": "start_calibrate_volume_high",
                    "dest": "save_calibrate_volume_high",
                },
                {
                    "trigger": "timeout",
                    "source": "save_calibrate_volume_high",
                    "dest": "turn_tuner_low",
                },
                {
                    "trigger": "next_step",
                    "source": "turn_tuner_low",
                    "dest": "start_calibrate_tuner_low",
                },
                {
                    "trigger": "timeout",
                    "source": "start_calibrate_tuner_low",
                    "dest": "save_calibrate_tuner_low",
                },
                {
                    "trigger": "timeout",
                    "source": "save_calibrate_tuner_low",
                    "dest": "turn_tuner_high",
                },
                {
                    "trigger": "next_step",
                    "source": "turn_tuner_high",
                    "dest": "start_calibrate_tuner_high",
                },
                {
                    "trigger": "timeout",
                    "source": "start_calibrate_tuner_high",
                    "dest": "save_calibrate_tuner_high",
                },
                {
                    "trigger": "timeout",
                    "source": "save_calibrate_tuner_high",
                    "dest": "save",
                },
                {"trigger": "timeout", "source": "save", "dest": "idle"},
            ],
            initial="idle",
            ignore_invalid_triggers=True,
        )

    def handle_turn_volume_low(self):
        self.write_message(u"Turn Volume Low and press Calibration button")

    def handle_start_calibrate_volume_low(self):
        self.write_message(u"Start Volume Low Calibration, Wait...")
        self.wait(2)
        self._queue_web.put({"cmd": self.state})

    def handle_save_calibrate_volume_low(self):
        self.write_message(u"Saving Volume Low")
        self._queue_web.put({"cmd": self.state})
        self.wait(0.5)

    def handle_turn_volume_high(self):
        self.write_message(u"Turn Volume High and press Calibration button")

    def handle_start_calibrate_volume_high(self):
        self.write_message(u"Start Volume High Calibration, Wait...")
        self.wait(2)
        self._queue_web.put({"cmd": self.state})

    def handle_save_calibrate_volume_high(self):
        self.write_message(u"Saving Volume High")
        self._queue_web.put({"cmd": self.state})
        self.wait(0.5)

    def handle_turn_tuner_low(self):
        self.write_message(u"Turn Tuner Low and press Calibration button")

    def handle_start_calibrate_tuner_low(self):
        self.write_message(u"Start Tuner Low Calibration, Wait...")
        self.wait(2)
        self._queue_web.put({"cmd": self.state})

    def handle_save_calibrate_tuner_low(self):
        self.write_message(u"Saving Tuner Low")
        self._queue_web.put({"cmd": self.state})
        self.wait(0.5)

    def handle_turn_tuner_high(self):
        self.write_message(u"Turn Tuner High and press Calibration button")

    def handle_start_calibrate_tuner_high(self):
        self.write_message(u"Start Tuner High Calibration, Wait...")
        self.wait(2)
        self._queue_web.put({"cmd": self.state})

    def handle_save_calibrate_tuner_high(self):
        self.write_message(u"Saving Tuner High")
        self._queue_web.put({"cmd": self.state})
        self.wait(0.5)

    def handle_save(self):
        self.write_message(u"Saving...")
        self._queue_web.put({"cmd": self.state})
        self.wait(0.5)

    def handle_done(self):
        self.write_message(u"Done !")

    def wait(self, seconds):
        timer = Timer(seconds, self.timeout)
        timer.start()

    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        if message == "next_step":
            self.next_step()

    def on_close(self):
        print("WebSocket closed")
