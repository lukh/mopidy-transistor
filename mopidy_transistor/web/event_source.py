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
            for ev in [
                "tuner_position",
                "tuner_labels",
                "battery_soc",
                "battery_charging",
            ]:
                if self._shared_data.get(
                    ev
                ) != SharedData.UNSET and self._sent_data.get(
                    ev
                ) != self._shared_data.get(
                    ev
                ):
                    self._sent_data.set(ev, self._shared_data.get(ev))

                    yield self.publish({ev: self._shared_data.get(ev)})

            t = self._shared_data.time
            d = self._shared_data.date
            if (
                t != SharedData.UNSET
                and d != SharedData.UNSET
                and self._shared_data.timestamp
            ):
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
                    yield self.publish(
                        {"time": dt.time().strftime("%H:%M:%S")}
                    )

                if dt.date() != self._sent_data.date:
                    self._sent_data.date = dt.date()

                    yield self.publish(
                        {"date": dt.date().strftime("%d/%m/%y")}
                    )

            yield gen.sleep(0.1)
