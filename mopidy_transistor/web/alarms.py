from .basics import BaseHandler

from dateutil import parser


class AlarmsHandler(BaseHandler):
    def initialize(self, queue_web):
        self._queue = queue_web

    def get(self):
        self.render("site/alarms.html", active_page="alarms", message="")

    def post(self):
        msg = ""
        date = self.get_argument("current_date")
        time = self.get_argument("current_time")
        try:
            dt = parser.parse(date + " " + time)
            self._queue.put({"cmd": "update_datetime", "dt": dt})
        except ValueError:
            msg = "Enter a Valid Date and Time"

        self.render("site/alarms.html", active_page="alarms", message=msg)
