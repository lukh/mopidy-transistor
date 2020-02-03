from threading import Lock
import subprocess

import datetime

class CommonSharedData(object):
    UNSET = "UNSET"
    def __init__(self, **kwargs):
        super(CommonSharedData, self).__setattr__('_lock', Lock())
        super(CommonSharedData, self).__setattr__('_attributes', kwargs)


    def __getattr__(self, name):
        if name not in self._attributes:
            super(CommonSharedData, self).__getattr__(name)

        return self.get(name)

    def __setattr__(self, name, value):
        if name not in self._attributes:
            super(CommonSharedData, self).__getattr__(name, value)
        return self.set(name, value)

    def get(self, name):
        if name not in self._attributes:
            raise KeyError(name)

        self._lock.acquire()
        val = self._attributes[name]
        self._lock.release()
        return val

    def set(self, name, value):
        if name not in self._attributes:
            raise KeyError(name)

        self._lock.acquire()
        self._attributes[name] = value
        self._lock.release()


class SharedData(CommonSharedData):
    def __init__(self):
        super(SharedData, self).__init__(
            tuner_position = 0,
            tuner_labels = {},
            time = datetime.time(0, 0, 0),
            date = datetime.date.max,
            battery_soc = 0,
            battery_charging = False,
            timestamp = 0
        )




def is_connected_to_internet():
    # ping google gateway
    cmd = "ping -q -w 1 -c 1 8.8.8.8 > /dev/null && echo ok || echo error"
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=None, shell=True)
    output, _ = process.communicate()

    return output.find(b"ok") != -1
