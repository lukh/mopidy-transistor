import tornado.ioloop
import tornado.web
from threading import Thread
import zmq
from ConfigParser import SafeConfigParser
from collections import OrderedDict

from tools import *


class MainHandler(tornado.web.RequestHandler):
    def initialize(self, dbfilename):
        self.db = RedBoxDataBase(dbfilename)

    def get(self):
        self.render("site/index.html", radios=self.db.getRadios(), feeds=self.db.getRssFeeds())
        

context = zmq.Context()



class AddRadioHandler(tornado.web.RequestHandler):
    def initialize(self, dbfilename):
        self.db = RedBoxDataBase(dbfilename)
        
        self.socket_tuner = context.socket(zmq.REQ)
        self.socket_tuner.setsockopt(zmq.LINGER, 0)
        self.socket_tuner.connect("ipc://tuner_position")


    def get(self):
        daemon_msg_recv = False
        self.socket_tuner.send("query:tuner_position")

        # use poll for timeouts:
        poller = zmq.Poller()
        poller.register(self.socket_tuner, zmq.POLLIN)
        if poller.poll(1*1000): # 1s timeout in milliseconds
            value = float(self.socket_tuner.recv())
            daemon_msg_recv= True
        else:
            value = 0.0

        self.render("site/add.html", add_type="Radio", tuner_position=value, daemon_msg_recv=daemon_msg_recv)

    def post(self):
        r = Radio(name=self.get_argument("name"), uri=self.get_argument("uri"), position=self.get_argument("position"))
        self.db.addRadio(r)

        self.socket_tuner.send("info:db_updated")

        # use poll for timeouts:
        poller = zmq.Poller()
        poller.register(self.socket_tuner, zmq.POLLIN)
        if poller.poll(1*1000): # 1s timeout in milliseconds
            msg = self.socket_tuner.recv()
        self.redirect("/redbox")


class EditRadioHandler(tornado.web.RequestHandler):
    def initialize(self, dbfilename):
        self.db = RedBoxDataBase(dbfilename)

    def get(self, radio_id):
        radio = self.db.getRadio(radio_id)
        self.render("site/edit.html", edit_type="Radio", element=radio)

    def post(self, radio_id):
        self.db.updateRadio(
            radio_id,
            self.get_argument('name'),
            self.get_argument('uri'),
            self.get_argument('position'),
        )
        self.redirect("/redbox")

class DeleteRadioHandler(tornado.web.RequestHandler):
    def initialize(self, dbfilename):
        self.db = RedBoxDataBase(dbfilename)

    def get(self, radio_id):
        self.db.deleteRadio(radio_id)
        self.redirect("/redbox")





class AddRssHandler(tornado.web.RequestHandler):
    def initialize(self, dbfilename):
        self.db = RedBoxDataBase(dbfilename)
        
        self.socket_tuner = context.socket(zmq.REQ)
        self.socket_tuner.setsockopt(zmq.LINGER, 0)
        self.socket_tuner.connect("ipc://tuner_position")


    def get(self):
        daemon_msg_recv = False
        self.socket_tuner.send("query:tuner_position")

        # use poll for timeouts:
        poller = zmq.Poller()
        poller.register(self.socket_tuner, zmq.POLLIN)
        if poller.poll(1*1000): # 1s timeout in milliseconds
            value = float(self.socket_tuner.recv())
            daemon_msg_recv= True
        else:
            value = 0.0

        self.render("site/add.html", add_type="RSS", tuner_position=value, daemon_msg_recv=daemon_msg_recv)

    def post(self):
        r = RssFeed(name=self.get_argument("name"), uri=self.get_argument("uri"), position=self.get_argument("position"))
        self.db.addRss(r)

        self.socket_tuner.send("info:db_updated")

        # use poll for timeouts:
        poller = zmq.Poller()
        poller.register(self.socket_tuner, zmq.POLLIN)
        if poller.poll(1*1000): # 1s timeout in milliseconds
            msg = self.socket_tuner.recv()
        self.redirect("/redbox")


class EditRssHandler(tornado.web.RequestHandler):
    def initialize(self, dbfilename):
        self.db = RedBoxDataBase(dbfilename)

    def get(self, rss_id):
        rss = self.db.getRss(rss_id)
        self.render("site/edit.html", edit_type="RSS", element=rss)

    def post(self, rss_id):
        self.db.updateRss(
            rss_id,
            self.get_argument('name'),
            self.get_argument('uri'),
            self.get_argument('position'),
        )
        self.redirect("/redbox")

class DeleteRssHandler(tornado.web.RequestHandler):
    def initialize(self, dbfilename):
        self.db = RedBoxDataBase(dbfilename)

    def get(self, rss_id):
        self.db.deleteRss(rss_id)
        self.redirect("/redbox")





class SettingsHandler(tornado.web.RequestHandler):
    def initialize(self, config_file):
        self.config_file = config_file

    def get(self, section=None):
        parser = SafeConfigParser()
        parser.read(self.config_file)

        config = OrderedDict()

        for section in parser.sections():
            if len(parser.items(section)) != 0:
                config[section] = OrderedDict()
                for name, value in parser.items(section):
                    config[section][name] = value

        self.render('site/settings.html', config=config)

    def post(self, section):
        parser = SafeConfigParser()
        parser.read(self.config_file)

        for name in parser.options(section):
            parser.set(section, name, self.get_argument(name))


        with open(self.config_file, 'w') as fp:
            parser.write(fp)

        self.redirect('/redbox/settings')
    
