from REDBoxMsg import REDBoxMsg

class REDBoxMasterRouter(object):
        # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    |
        # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
        # |   |   |   |   |   |   |Sy |Ms  ||   |   |   |   |   |   |   |    ||   |   |   |   |   |   |   |    |
        @staticmethod
        def makeQueryProtocolVersion():
            msg = REDBoxMsg()


            msg.setMsgType(REDBoxMsg.MsgType.MsgType_System)
            msg.setSystem(REDBoxMsg.System.System_QueryProtocolVersion)


            return msg
 



        def processPotentiometerVolume(self, in_potentiometervalue):
            raise NotImplementedError

        def processPotentiometerTuner(self, in_potentiometervalue):
            raise NotImplementedError


        def processSwitch(self, in_switchindex, in_switchvalue):
            raise NotImplementedError

        def processSendProtocolVersion(self, in_sendprotocolversionmajor, in_sendprotocolversionminor):
            raise NotImplementedError




        def process(self, in_msg):
            if in_msg.getMsgType() == REDBoxMsg.MsgType.MsgType_UserAction:
                if in_msg.getUserAction() == REDBoxMsg.UserAction.UserAction_Potentiometer:
                    if msg.getPotentiometer() == REDBoxMsg.Potentiometer.Potentiometer_Volume:
                        processPotentiometerVolume(in_msg.getPotentiometerValue())
                    elif msg.getPotentiometer() == REDBoxMsg.Potentiometer.Potentiometer_Tuner:
                        processPotentiometerTuner(in_msg.getPotentiometerValue())


                elif in_msg.getUserAction() == REDBoxMsg.UserAction.UserAction_Switch:
                    processSwitch(in_msg.getSwitchIndex(), in_msg.getSwitchValue())




            elif in_msg.getMsgType() == REDBoxMsg.MsgType.MsgType_System:
                if in_msg.getSystem() == REDBoxMsg.System.System_QueryProtocolVersion:
                    pass

                elif in_msg.getSystem() == REDBoxMsg.System.System_SendProtocolVersion:
                    processSendProtocolVersion(in_msg.getSendProtocolVersionMajor(), in_msg.getSendProtocolVersionMinor())





