import datetime
import time
import json
from tornado import websocket
import tornado.ioloop

import json
from mopidy_transistor.utils import SharedData

class EventSource(websocket.WebSocketHandler):
    def initialize(self, shared_data):
        self.shared_data = shared_data

    def open(self):
        self.sched = tornado.ioloop.PeriodicCallback(self.callback, 100)
        self.sched.start()

    def on_close(self):
        self.sched.stop()

    def callback(self):
        d = self.shared_data.get_data()
        if len(d) != 0:
            try:
                self.write_message(json.dumps(d))
            except websocket.WebSocketClosedError:
                pass
