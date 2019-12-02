import datetime
import time
from tornado import web, gen
from tornado.iostream import StreamClosedError
import json
from mopidy_transistor.utils import SharedData


class EventSource(web.RequestHandler):
    """Basic handler for server-sent events."""

    def initialize(self, shared_data):
        self._shared_data = shared_data

        self._sent_data = SharedData()

        self.set_header("content-type", "text/event-stream")
        self.set_header("cache-control", "no-cache")

        self._stop = False

    def on_connection_close(self):
        self._stop = True

    @gen.coroutine
    def publish(self, data):
        """Pushes data to a listener."""
        try:
            self.write("data: {}\n\n".format(json.dumps(data)))
            yield self.flush()
        except StreamClosedError:
            pass

    @gen.coroutine
    def get(self):
        while not self._stop:
            if self._sent_data.tuner_position != self._shared_data.tuner_position:
                self._sent_data.tuner_position = self._shared_data.tuner_position

                yield self.publish({"tuner_position": self._shared_data.tuner_position})

            if self._sent_data.tuner_labels != self._shared_data.tuner_labels:
                self._sent_data.tuner_labels = self._shared_data.tuner_labels

                yield self.publish({"tuner_labels": self._shared_data.tuner_labels})

            if self._sent_data.date != self._shared_data.date:
                self._sent_data.date = self._shared_data.date

                yield self.publish(
                    {"date": self._shared_data.date.strftime("%d/%m/%y")}
                )

            if self._sent_data.battery_soc != self._shared_data.battery_soc:
                self._sent_data.battery_soc = self._shared_data.battery_soc

                yield self.publish({"battery_soc": self._shared_data.battery_soc})

            yield gen.sleep(0.1)

            t = self._shared_data.time
            d = self._shared_data.date

            try:
                dt = datetime.datetime(
                    d.year, d.month, d.day, t.hour, t.minute, t.second
                )
                dt += datetime.timedelta(
                    seconds=int(time.time() - self._shared_data.timestamp)
                )
            except OverflowError:
                dt = datetime.datetime.max

            if dt.time() != self._sent_data.time:
                self._sent_data.time = dt.time()
                yield self.publish({"time": dt.time().strftime("%H:%M:%S")})
