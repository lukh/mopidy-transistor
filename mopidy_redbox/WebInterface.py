import tornado.ioloop
import tornado.web


from tools import *


class MainHandler(tornado.web.RequestHandler):
    def initialize(self, dbfilename):
        self.db = RedBoxDataBase(dbfilename)

    def get(self):
        self.render("index.html", radios=self.db.getRadios())
        

class AddHandler(tornado.web.RequestHandler):
    def initialize(self, dbfilename):
        self.db = RedBoxDataBase(dbfilename)

    def get(self):
        self.render("add.html")

    def post(self):
        r = Radio(name=self.get_argument("name"), uri=self.get_argument("uri"), position=0.69)
        self.db.addRadio(r)

        self.redirect("/redbox")


class EditHandler(tornado.web.RequestHandler):
    def initialize(self, dbfilename):
        self.db = RedBoxDataBase(dbfilename)

    def get(self, radio_id):
        self.redirect("/")

class DeleteHandler(tornado.web.RequestHandler):
    def initialize(self, dbfilename):
        self.db = RedBoxDataBase(dbfilename)

    def get(self, radio_id):
        self.db.deleteRadio(radio_id)
        self.redirect("/redbox")


