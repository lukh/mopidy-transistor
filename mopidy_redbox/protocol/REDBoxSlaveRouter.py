from REDBoxMsg import REDBoxMsg

class REDBoxSlaveRouter(object):
        # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    |
        # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
        # |   |   |   |   |   |Po |Us |Ms  ||Va |Va |Va |Va |Va |Va |Va |Va  ||Va |Va |Va |Va |Va |Va |Va |Va  |
        # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    |
        # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
        # |   |   |   |   |   |Po |Us |Ms  ||Va |Va |Va |Va |Va |Va |Va |Va  ||Va |Va |Va |Va |Va |Va |Va |Va  |
        @staticmethod
        def makePotentiometerVolume(in_potentiometervalue):
            msg = REDBoxMsg()


            msg.setMsgType(REDBoxMsg.MsgType.MsgType_UserAction)
            msg.setUserAction(REDBoxMsg.UserAction.UserAction_Potentiometer)

            msg.setPotentiometer(REDBoxMsg.Potentiometer.Potentiometer_Volume)

            msg.setPotentiometerValue(in_potentiometervalue)

            return msg

        # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    |
        # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
        # |   |   |   |   |   |Po |Us |Ms  ||Va |Va |Va |Va |Va |Va |Va |Va  ||Va |Va |Va |Va |Va |Va |Va |Va  |
        @staticmethod
        def makePotentiometerTuner(in_potentiometervalue):
            msg = REDBoxMsg()


            msg.setMsgType(REDBoxMsg.MsgType.MsgType_UserAction)
            msg.setUserAction(REDBoxMsg.UserAction.UserAction_Potentiometer)

            msg.setPotentiometer(REDBoxMsg.Potentiometer.Potentiometer_Tuner)

            msg.setPotentiometerValue(in_potentiometervalue)

            return msg


 

        # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    |
        # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
        # |Va |Va |Id |Id |Id |Id |Us |Ms  ||   |   |   |   |   |   |Va |Va  ||   |   |   |   |   |   |   |    |
        @staticmethod
        def makeSwitch(in_switchindex, in_switchvalue):
            msg = REDBoxMsg()


            msg.setMsgType(REDBoxMsg.MsgType.MsgType_UserAction)
            msg.setUserAction(REDBoxMsg.UserAction.UserAction_Switch)

            msg.setSwitchIndex(in_switchindex)
            msg.setSwitchValue(in_switchvalue)

            return msg
 

        # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    |
        # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
        # |Mi |Mi |Ma |Ma |Ma |Ma |Sy |Ms  ||   |   |   |   |   |   |Mi |Mi  ||   |   |   |   |   |   |   |    |
        @staticmethod
        def makeSendProtocolVersion(in_sendprotocolversionmajor, in_sendprotocolversionminor):
            msg = REDBoxMsg()


            msg.setMsgType(REDBoxMsg.MsgType.MsgType_System)
            msg.setSystem(REDBoxMsg.System.System_SendProtocolVersion)

            msg.setSendProtocolVersionMajor(in_sendprotocolversionmajor)
            msg.setSendProtocolVersionMinor(in_sendprotocolversionminor)

            return msg
 



        def processQueryProtocolVersion(self, ):
            raise NotImplementedError




        def process(self, in_msg):
            if in_msg.getMsgType() == REDBoxMsg.MsgType.MsgType_UserAction:
                pass

            elif in_msg.getMsgType() == REDBoxMsg.MsgType.MsgType_System:
                if in_msg.getSystem() == REDBoxMsg.System.System_QueryProtocolVersion:
                    processQueryProtocolVersion()


                elif in_msg.getSystem() == REDBoxMsg.System.System_SendProtocolVersion:
                    pass




