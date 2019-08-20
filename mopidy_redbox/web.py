import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def initialize(self):
        pass

    def get(self):
        self.render("site/index.html", page="index")
        

class BrowseHandler(tornado.web.RequestHandler):
    def initialize(self, core):
        self.core = core

    def get(self):
        self.render("site/browse.html", page="browse")
