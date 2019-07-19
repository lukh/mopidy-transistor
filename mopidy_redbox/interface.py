import time
import serial
from threading import Thread
from mopidy.exceptions import FrontendError

class SerialInterfaceListener(Thread):
    def __init__(self, config):
        super(SerialInterfaceListener, self).__init__()

        self._stop_flag = False


        # opening serial port
        try:
            # rtscts=True,dsrdtr=True is for virtual port (using socat)
            self.serial = serial.Serial(config['redbox']['serial_port'], int(config['redbox']['serial_baudrate']), timeout=0.1, rtscts=False, dsrdtr=False)
        except Exception as e:
            raise FrontendError("Impossible to open serial port {}: {}".format(config['redbox']['serial_port'], str(e)))
        
        
    @property
    def stop(self):
        return self._stop_flag

    @stop.setter
    def stop(self, st):
        self._stop_flag = st

    def run(self):
        while not self.stop:
            raw_byte = self.serial.read()
            if raw_byte == "":
                continue

            print raw_byte

            