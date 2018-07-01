import tornado.ioloop
import tornado.web
from threading import Thread
import zmq

from tools import *


class MainHandler(tornado.web.RequestHandler):
    def initialize(self, dbfilename):
        self.db = RedBoxDataBase(dbfilename)

    def get(self):
        self.render("site/index.html", radios=self.db.getRadios())
        

context = zmq.Context()
class AddHandler(tornado.web.RequestHandler):
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

        self.render("site/add.html", tuner_position=value, daemon_msg_recv=daemon_msg_recv)

    def post(self):
        r = Radio(name=self.get_argument("name"), uri=self.get_argument("uri"), position=self.get_argument("position"))
        self.db.addRadio(r)

        self.socket_tuner.send("info:db_updated")

        # use poll for timeouts:
        poller = zmq.Poller()
        poller.register(self.socket_tuner, zmq.POLLIN)
        if poller.poll(1*1000): # 1s timeout in milliseconds
            msg = float(self.socket_tuner.recv())

        self.redirect("/redbox")


class EditHandler(tornado.web.RequestHandler):
    def initialize(self, dbfilename):
        self.db = RedBoxDataBase(dbfilename)

    def get(self, radio_id):
        radio = self.db.getRadio(radio_id)
        self.render("site/edit.html", radio=radio)

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


