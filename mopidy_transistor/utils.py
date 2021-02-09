from threading import Lock
import subprocess


class CommonSharedData(object):
    UNSET = "UNSET"

    def __init__(self, **kwargs):
        super().__init__()

        super(CommonSharedData, self).__setattr__("_lock", Lock())
        super(CommonSharedData, self).__setattr__("_attributes", kwargs)
        super(CommonSharedData, self).__setattr__("_updated", {k:False for k in kwargs})

    def __getattr__(self, name):
        if name not in self._attributes:
            super(CommonSharedData, self).__getattr__(name)

        return self.get(name)

    def __setattr__(self, name, value):
        if name not in self._attributes:
            super(CommonSharedData, self).__setattr__(name, value)
        return self.set(name, value)

    def get(self, name):
        if name not in self._attributes:
            raise KeyError(name)

        self._lock.acquire()
        val = self._attributes[name]
        self._updated[name] = False
        self._lock.release()
        return val

    def set(self, name, value):
        if name not in self._attributes:
            raise KeyError(name)

        self._lock.acquire()
        self._attributes[name] = value
        self._updated[name] = True
        self._lock.release()

    def get_data(self):
        self._lock.acquire()

        data =  {k:self._attributes[k] for k in self._attributes if self._updated[k] == True}
        
        for k in self._updated: self._updated[k] = False

        self._lock.release()

        return data


class SharedData(CommonSharedData):
    def __init__(self):
        super(SharedData, self).__init__(
            tuner_position=self.UNSET,
            tuner_labels=self.UNSET,
            time=self.UNSET,
            date=self.UNSET,
            battery_soc=self.UNSET,
            battery_charging=self.UNSET,
        )


def is_connected_to_internet():
    # ping google gateway
    cmd = "ping -q -w 1 -c 1 8.8.8.8 > /dev/null && echo ok || echo error"
    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=None, shell=True
    )
    output, _ = process.communicate()

    return output.find(b"ok") != -1
