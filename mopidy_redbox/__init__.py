from __future__ import unicode_literals

import logging
import os

from mopidy import config, ext
import tornado.web
from WebInterface import *


__version__ = '0.0.1'

# TODO: If you need to log, use loggers named after the current Python module
logger = logging.getLogger(__name__)


class Extension(ext.Extension):

    dist_name = 'Mopidy-Redbox'
    ext_name = 'redbox'
    version = __version__

    def get_default_config(self):
        conf_file = os.path.join(os.path.dirname(__file__), 'ext.conf')
        default_conf = config.read(conf_file)
        default_conf = default_conf.replace("~", os.path.expanduser("~"))

        return default_conf

    def get_config_schema(self):
        schema = super(Extension, self).get_config_schema()
        schema['serial_port'] = config.String()
	schema['serial_baudrate'] = config.String()
        schema['dbfile'] = config.String()
        schema['fm_noise_directory'] = config.String()
        schema['config_file'] = config.String()
        return schema

    def webapp(self, config, core):

        return [
            (r"/", MainHandler, dict(dbfilename=config['redbox']['dbfile'])),

            (r"/radio/add", AddRadioHandler, dict(dbfilename=config['redbox']['dbfile'])),
            (r"/radio/edit/([0-9]+)", EditRadioHandler, dict(dbfilename=config['redbox']['dbfile'])),
            (r"/radio/delete/([0-9]+)", DeleteRadioHandler, dict(dbfilename=config['redbox']['dbfile'])),

            (r"/rss/add", AddRssHandler, dict(dbfilename=config['redbox']['dbfile'])),
            (r"/rss/edit/([0-9]+)", EditRssHandler, dict(dbfilename=config['redbox']['dbfile'])),
            (r"/rss/delete/([0-9]+)", DeleteRssHandler, dict(dbfilename=config['redbox']['dbfile'])),

            (r"/rss/show/([0-9]+)", ShowRssHandler, dict(dbfilename=config['redbox']['dbfile'])),

            (r"/settings", SettingsHandler, dict(config_file=config['redbox']['config_file'])),
            (r"/settings/([^/]+)", SettingsHandler, dict(config_file=config['redbox']['config_file'])),

            (r'/css/(.*)', tornado.web.StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'site/css')}),
            (r'/vendor/(.*)', tornado.web.StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'site/vendor')}),
            (r'/images/(.*)', tornado.web.StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'site/images')})
        ]

    def setup(self, registry):
        registry.add('http:app', {
            'name': self.ext_name,
            'factory': self.webapp
        })

        from .ControlFrontend import ControlFrontend
        registry.add('frontend', ControlFrontend)




