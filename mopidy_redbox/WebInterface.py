import tornado.ioloop
import tornado.web
from threading import Thread
import zmq

from tools import *


class MainHandler(tornado.web.RequestHandler):
    def initialize(self, dbfilename):
        self.db = RedBoxDataBase(dbfilename)

    def get(self):
        self.render("index.html", radios=self.db.getRadios())
        

context = zmq.Context()
class AddHandler(tornado.web.RequestHandler):
    def initialize(self, dbfilename):
        self.db = RedBoxDataBase(dbfilename)
        
        self.socket_tuner = context.socket(zmq.REQ)
        self.socket_tuner.connect("ipc://tuner_position")


    def get(self):
        self.socket_tuner.send("query:tuner_position")
        value = float(self.socket_tuner.recv())

        self.render("add.html", tuner_position=value)

    def post(self):
        r = Radio(name=self.get_argument("name"), uri=self.get_argument("uri"), position=0.69)
        self.db.addRadio(r)

        self.redirect("/redbox")


class EditHandler(tornado.web.RequestHandler):
    def initialize(self, dbfilename):
        self.db = RedBoxDataBase(dbfilename)

    def get(self, radio_id):
        radio = self.db.getRadio(radio_id)
        self.render("edit.html", radio=radio)

    def post(self, radio_id):
        self.db.updateRadio(
            radio_id,
            self.get_argument('name'),
            self.get_argument('uri'),
            self.get_argument('position'),
        )
        self.redirect("/redbox")

class DeleteHandler(tornado.web.RequestHandler):
    def initialize(self, dbfilename):
        self.db = RedBoxDataBase(dbfilename)

    def get(self, radio_id):
        self.db.deleteRadio(radio_id)
        self.redirect("/redbox")


