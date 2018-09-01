import tornado.ioloop
import tornado.web
from threading import Thread
from ConfigParser import SafeConfigParser
from collections import OrderedDict
import podcastparser
import urllib
from multiprocessing.connection import Client

from tools import *


class MainHandler(tornado.web.RequestHandler):
    def initialize(self, dbfilename):
        self.db = RedBoxDataBase(dbfilename)

    def get(self):
        self.render("site/index.html", radios=self.db.getRadios(), feeds=self.db.getRssFeeds())
        


class AddRadioHandler(IAddHandler):
    ADD_TYPE = "Radio"
    def post_action(self):
        r = Radio(name=self.get_argument("name"), uri=self.get_argument("uri"), position=self.get_argument("position"))
        self.db.addRadio(r)


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





class AddRssHandler(IAddHandler):
    ADD_TYPE = "RSS"
    def post_action(self):
        r = RssFeed(name=self.get_argument("name"), uri=self.get_argument("uri"), position=self.get_argument("position"))
        self.db.addRss(r)


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



class ShowRssHandler(tornado.web.RequestHandler):
    def initialize(self, dbfilename):
        self.db = RedBoxDataBase(dbfilename)

    def get(self, rss_id):
        rss = self.db.getRss(rss_id)

        parsed = podcastparser.parse(rss.uri, urllib.urlopen(rss.uri))

        self.render("site/show_rss.html", parsed=parsed)




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
        # all internal settings
        if section != "wifi":
            parser = SafeConfigParser()
            parser.read(self.config_file)

            for name in parser.options(section):
                parser.set(section, name, self.get_argument(name))


            with open(self.config_file, 'w') as fp:
                parser.write(fp)

        # wifi
        else:
            pass 

        # redirect the to settings page
        self.redirect('/redbox/settings')
