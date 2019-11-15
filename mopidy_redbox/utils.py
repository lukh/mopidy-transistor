from queue import Queue


class ConsumerQueue(Queue):
    def __init__(self, idx, parent, **kargs):
        Queue.__init__(self, **kargs)
        self._idx = idx
        self._parent = parent

    def detach(self):
        self._parent.detach(self._idx)

class MultiConsumerQueue(object):
    def __init__(self):
        self._idx = 0
        self._queues = {}

    def make(self):
        queue = ConsumerQueue(self._idx, self)
        self._queues[self._idx] = queue
        self._idx += 1

        return queue

    def detach(self, idx):
        del self._queues[idx]

    def put(self, item):
        for q in self._queues.values():
            q.put(item)
