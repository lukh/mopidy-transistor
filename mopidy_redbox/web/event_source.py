from tornado import web, gen
from tornado.ioloop import PeriodicCallback
from tornado.iostream import StreamClosedError
import json


class EventSource(web.RequestHandler):
    """Basic handler for server-sent events."""
    def initialize(self, queue):
        self._queue = queue
        self.set_header('content-type', 'text/event-stream')
        self.set_header('cache-control', 'no-cache')

    @gen.coroutine
    def publish(self, data):
        """Pushes data to a listener."""
        try:
            self.write('data: {}\n\n'.format(json.dumps(data)))
            yield self.flush()
        except StreamClosedError:
            pass

    @gen.coroutine
    def get(self):
        while True:
            while not self._queue.empty():
                yield self.publish(self._queue.get())
            else:
                yield gen.sleep(0.1)


