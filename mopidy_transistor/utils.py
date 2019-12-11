from threading import Lock
import subprocess

import datetime


class SharedData(object):
    def __init__(self):
        self._lock = Lock()

        self._tuner_position = 0
        self._tuner_labels = []
        self._time = datetime.time(0, 0, 0)
        self._date = datetime.date.max
        self._battery_soc = 0

        self._timestamp = 0

    @property
    def tuner_position(self):
        self._lock.acquire()
        data = self._tuner_position
        self._lock.release()
        return data

    @tuner_position.setter
    def tuner_position(self, tp):
        self._lock.acquire()
        self._tuner_position = tp
        self._lock.release()

    @property
    def tuner_labels(self):
        self._lock.acquire()
        data = self._tuner_labels
        self._lock.release()
        return data

    @tuner_labels.setter
    def tuner_labels(self, tl):
        self._lock.acquire()
        self._tuner_labels = tl
        self._lock.release()

    @property
    def time(self):
        self._lock.acquire()
        data = self._time
        self._lock.release()
        return data

    @time.setter
    def time(self, t):
        self._lock.acquire()
        self._time = t
        self._lock.release()

    @property
    def date(self):
        self._lock.acquire()
        data = self._date
        self._lock.release()
        return data

    @date.setter
    def date(self, d):
        self._lock.acquire()
        self._date = d
        self._lock.release()

    @property
    def battery_soc(self):
        self._lock.acquire()
        data = self._battery_soc
        self._lock.release()
        return data

    @battery_soc.setter
    def battery_soc(self, tp):
        self._lock.acquire()
        self._battery_soc = tp
        self._lock.release()

    @property
    def timestamp(self):
        self._lock.acquire()
        data = self._timestamp
        self._lock.release()
        return data

    @timestamp.setter
    def timestamp(self, tp):
        self._lock.acquire()
        self._timestamp = tp
        self._lock.release()


def is_connected_to_internet():
    # ping google gateway
    cmd = "ping -q -w 1 -c 1 8.8.8.8 > /dev/null && echo ok || echo error"
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=None, shell=True)
    output, _ = process.communicate()

    return output.find(b"ok") != -1
