import bcrypt

import tornado.web

from mopidy_transistor import utils


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

    def get_login_url(self):
        return "login"


class MainHandler(BaseHandler):
    def initialize(self):
        pass

    def get(self):
        if utils.is_connected_to_internet():
            self.render("site/index.html", active_page="index")
        else:
            self.redirect("wifi")


class AboutHandler(BaseHandler):
    def initialize(self):
        pass

    def get(self):
        self.render("site/about.html", active_page="about")


class BrowseHandler(BaseHandler):
    def initialize(self):
        pass

    def get(self):
        self.render("site/browse.html", active_page="browse")


class LoginHandler(BaseHandler):
    def initialize(self, config):
        self._user = config["transistor"]["user"]
        self._hashed_passwd = config["transistor"]["passwd"]

    def get(self):
        if self._user is None and self._hashed_passwd is None:
            self.set_secure_cookie("user", "none")
            self.redirect(self.get_argument("next", "/"))
        else:
            self.render(
                "site/login.html",
                active_page="login",
                next=self.get_argument("next", "/"),
                error_msg=None,
            )

    def post(self):
        user = self.get_argument("user")
        raw_passwd = str(self.get_argument("passwd"))

        if (self._user is None and self._hashed_passwd is None) or (
            user == self._user and bcrypt.checkpw(raw_passwd, str(self._hashed_passwd))
        ):
            self.set_secure_cookie("user", user)
            self.redirect(self.get_argument("next", "/"))

        else:
            self.render(
                "site/login.html",
                active_page="login",
                next=self.get_argument("next", "/"),
                error_msg="Can't Log In...",
            )
