import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def initialize(self):
        pass

    def get(self):
        self.render("site/index.html")
        

class BrowseHandler(tornado.web.RequestHandler):
    def initialize(self, core):
        self.core = core

    def get(self):
        uri = None
        data = self.core.library.browse(uri).get()
        self.render("site/browse.html", data=data)
