from tornado import web, gen
from tornado.ioloop import PeriodicCallback
from tornado.iostream import StreamClosedError

from ..interface import shared_data

def make_source():
    data_publisher = DataSource({})

    def get_next():
        data_publisher.data = {"tuner_position":shared_data.tuner_position, "tuner_labels":shared_data.tuner_labels, "battery_status":shared_data.battery_status}

    checker = PeriodicCallback(get_next, 100.)
    checker.start()

    return data_publisher


class DataSource(object):
    """Generic object for producing data to feed to clients."""
    def __init__(self, initial_data=None):
        self._data = initial_data
    
    @property
    def data(self):
        return self._data
        
    @data.setter
    def data(self, new_data):
        self._data = new_data

class EventSource(web.RequestHandler):
    """Basic handler for server-sent events."""
    def initialize(self, source):
        """The ``source`` parameter is a string that is updated with
        new data. The :class:`EventSouce` instance will continuously
        check if it is updated and publish to clients when it is.
        """
        self.source = source
        self._last = None
        self.set_header('content-type', 'text/event-stream')
        self.set_header('cache-control', 'no-cache')

    @gen.coroutine
    def publish(self, data):
        """Pushes data to a listener."""
        try:
            self.write('data: {}\n\n'.format(data))
            yield self.flush()
        except StreamClosedError:
            pass

    @gen.coroutine
    def get(self):
        while True:
            if self.source.data != self._last:
                yield self.publish(self.source.data)
                self._last = self.source.data
            else:
                yield gen.sleep(0.1)


