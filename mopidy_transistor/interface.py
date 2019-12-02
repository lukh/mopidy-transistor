import time
import serial
from threading import Thread, Lock
import logging

from microparcel import microparcel as mp

from .protocol.TransistorMsg import TransistorMsg


logger = logging.getLogger(__name__)


class SerialInterfaceListener(Thread):
    def __init__(self, frontend, config):
        super(SerialInterfaceListener, self).__init__()

        self._stop_flag = False

        self.frontend = frontend

        self.initCommunication(
            config["transistor"]["serial_port"],
            int(config["transistor"]["serial_baudrate"]),
        )

    @property
    def stop(self):
        return self._stop_flag

    @stop.setter
    def stop(self, st):
        self._stop_flag = st

    def initCommunication(self, serial_port, serial_baudrate):
        self._mutex = Lock()
        # opening serial port
        try:
            # rtscts=True,dsrdtr=True is for virtual port (using socat)
            self.serial = serial.Serial(serial_port, serial_baudrate, timeout=0.1)
        except serial.SerialException as e:
            self.serial = None
            logger.error(
                "Can't open serial port {} @ {}: {}".format(
                    serial_port, serial_baudrate, str(e)
                )
            )
            logger.warning(
                "It is not possible to communicate with the hardware, but the web front end still work"
            )
            # raise FrontendError("Impossible to open serial port {}: {}".format(serial_port, str(e)))

        self._parser = mp.make_parser_cls(TransistorMsg().size)()

    def run(self):
        if self.serial is None:
            return

        while not self.stop:
            ser_in = self.serial.read()
            if len(ser_in) == 0:
                continue

            raw_byte = ord(ser_in)

            msg = TransistorMsg()

            # parse byte
            status = self._parser.parse(raw_byte, msg)
            if status == self._parser.Status.Complete:
                self.frontend.process_serial_message(msg)
            if status == self._parser.Status.Error:
                logger.error(
                    "Error in parsing Serial Message: recv byte = {}, current msg = {}".format(
                        raw_byte, msg.data
                    )
                )

        self.serial.close()

    def sendMsg(self, msg):
        if self.serial is None:
            logger.warning("Can't send message to the hardware, serial port not opened")
            return

        self._mutex.acquire()
        frame = self._parser.encode(msg)
        buff = bytearray()
        for d in frame.data:
            buff.append(d)
        self.serial.write(buff)
        self._mutex.release()


class WebsocketInterfaceListener(Thread):
    def __init__(self, frontend, queue_web):
        super(WebsocketInterfaceListener, self).__init__()

        self._stop_flag = False

        self._frontend = frontend
        self._queue_web = queue_web

    @property
    def stop(self):
        return self._stop_flag

    @stop.setter
    def stop(self, st):
        self._stop_flag = st

    def run(self):
        while not self.stop:
            while not self._queue_web.empty():
                self._frontend.process_queue_web(self._queue_web.get())

            else:
                time.sleep(0.1)
