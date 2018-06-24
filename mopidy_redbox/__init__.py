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
        return config.read(conf_file)

    def get_config_schema(self):
        schema = super(Extension, self).get_config_schema()
        schema['serial_port'] = config.String()
        schema['dbfile'] = config.String()
        schema['fm_noise_directory'] = config.String()
        return schema

    def webapp(self, config, core):

        return [
            (r"/", MainHandler, dict(dbfilename=config['redbox']['dbfile'])),
            (r"/add", AddHandler, dict(dbfilename=config['redbox']['dbfile'])),
            (r"/edit/([0-9]+)", EditHandler, dict(dbfilename=config['redbox']['dbfile'])),
            (r"/delete/([0-9]+)", DeleteHandler, dict(dbfilename=config['redbox']['dbfile'])),
            (r'/css/(.*)', tornado.web.StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'css')}),
            (r'/vendor/(.*)', tornado.web.StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'vendor')}),
            (r'/images/(.*)', tornado.web.StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'images')})
        ]

    def setup(self, registry):
        registry.add('http:app', {
            'name': self.ext_name,
            'factory': self.webapp
        })

        from .ControlFrontend import ControlFrontend
        registry.add('frontend', ControlFrontend)
