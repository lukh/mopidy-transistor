from microparcel import microparcel as mp
from mopidy_transistor.protocol.TransistorMsg import TransistorMsg
from mopidy_transistor.protocol.TransistorSlaveRouter import TransistorSlaveRouter
import serial

ser = serial.Serial("/dev/pts/5", 115200, timeout=0.1)
router = TransistorSlaveRouter()
parser = mp.make_parser_cls(TransistorMsg().size)()


def send_msg(msg):
    frame = parser.encode(msg)
    print frame
    ser.write(frame.data)


if __name__ == "__main__":
    while True:
        raw = raw_input("What do you want ?")
        try:
            if raw == "radio":
                msg = router.makeSwitchRadio()
                send_msg(msg)

            elif raw == "podcast":
                msg = router.makeSwitchPodcast()
                send_msg(msg)

            elif raw == "power":
                msg = router.makeSwitchPower()
                send_msg(msg)

            elif raw == "next":
                msg = router.makeSwitchNext()
                send_msg(msg)

            elif raw == "previous":
                msg = router.makeSwitchPrevious()
                send_msg(msg)

            else:
                cmd, val = raw.split(":")
                print cmd, val

                if cmd == "vol":
                    msg = router.makePotentiometerVolume(int(val))
                    send_msg(msg)

                if cmd == "tun":
                    msg = router.makePotentiometerTuner(int(val))
                    send_msg(msg)

        except Exception as e:
            print str(e)
            break
