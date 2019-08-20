from microparcel import microparcel as mp
from mopidy_redbox.protocol.REDBoxMsg import REDBoxMsg
from mopidy_redbox.protocol.REDBoxSlaveRouter import REDBoxSlaveRouter
import serial

ser = serial.Serial("/dev/pts/5", 115200, timeout=0.1)
router = REDBoxSlaveRouter()
parser = mp.make_parser_cls(REDBoxMsg().size)()

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



    

