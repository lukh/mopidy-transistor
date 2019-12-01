from __future__ import unicode_literals

import logging
import os

import pkg_resources

import tornado.web

from mopidy import config, ext

from . import web


__version__ = pkg_resources.get_distribution("Mopidy-Transistor").version

# TODO: If you need to log, use loggers named after the current Python module
logger = logging.getLogger(__name__)


class Extension(ext.Extension):

    dist_name = "Mopidy-Transistor"
    ext_name = "transistor"
    version = __version__

    def get_default_config(self):
        conf_file = os.path.join(os.path.dirname(__file__), "ext.conf")
        default_conf = config.read(conf_file)
        default_conf = default_conf.replace("~", os.path.expanduser("~"))

        return default_conf

    def get_config_schema(self):
        schema = super(Extension, self).get_config_schema()
        schema["serial_port"] = config.String()
        schema["serial_baudrate"] = config.Integer()

        schema["podcasts_timeout"] = config.Integer()

        schema["noise_folder"] = config.Path()

        schema["config_file"] = config.Path()

        schema["user"] = config.String(optional=True)
        schema["passwd"] = config.String(optional=True)

        return schema

    def setup(self, registry):
        from .backend import TransistorBackend

        registry.add("backend", TransistorBackend)

        from .frontend import TransistorFrontend

        self._shared_data = TransistorFrontend.shared_data
        self._queue_front = TransistorFrontend.queue_front
        self._queue_web = TransistorFrontend.queue_web

        registry.add("frontend", TransistorFrontend)

        registry.add("http:app", {"name": self.ext_name, "factory": self.web_factory})

    def web_factory(self, config, core):
        return [
            ("/", web.MainHandler, {}),
            ("/browse", web.BrowseHandler, {}),
            ("/radios", web.RadioHandler, {"core": core, "config": config}),
            ("/podcasts", web.PodcastHandler, {"core": core, "config": config}),
            ("/about", web.AboutHandler, {}),
            ("/settings", web.SettingsHandler, {"config": config}),
            ("/alarms", web.AlarmsHandler, {"queue_web": self._queue_web}),
            ("/wifi", web.WifiHandler, {}),
            ("/update", web.UpdateHandler, {}),
            ("/updatesocket", web.UpdateWebSocketHandler, {}),
            ("/login", web.LoginHandler, {"config": config}),
            ("/calibration", web.CalibrationHandler, {}),
            ("/events", web.EventSource, {"shared_data": self._shared_data}),
            (
                "/calibsocket",
                web.CalibrationWebSocketHandler,
                {"queue_front": self._queue_front, "queue_web": self._queue_web},
            ),
            (
                r"/(.*)",
                tornado.web.StaticFileHandler,
                {"path": os.path.join(os.path.dirname(__file__), "web", "site")},
            ),
        ]
