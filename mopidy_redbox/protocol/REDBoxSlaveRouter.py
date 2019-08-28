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
        # |   |   |   |Sw |Sw |Sw |Us |Ms  ||   |   |   |   |   |   |   |    ||   |   |   |   |   |   |   |    |
        # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    |
        # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
        # |   |   |   |Sw |Sw |Sw |Us |Ms  ||   |   |   |   |   |   |   |    ||   |   |   |   |   |   |   |    |
        @staticmethod
        def makeSwitchPower():
            msg = REDBoxMsg()


            msg.setMsgType(REDBoxMsg.MsgType.MsgType_UserAction)
            msg.setUserAction(REDBoxMsg.UserAction.UserAction_Switch)

            msg.setSwitch(REDBoxMsg.Switch.Switch_Power)


            return msg

        # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    |
        # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
        # |   |   |   |Sw |Sw |Sw |Us |Ms  ||   |   |   |   |   |   |   |    ||   |   |   |   |   |   |   |    |
        @staticmethod
        def makeSwitchRadio():
            msg = REDBoxMsg()


            msg.setMsgType(REDBoxMsg.MsgType.MsgType_UserAction)
            msg.setUserAction(REDBoxMsg.UserAction.UserAction_Switch)

            msg.setSwitch(REDBoxMsg.Switch.Switch_Radio)


            return msg

        # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    |
        # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
        # |   |   |   |Sw |Sw |Sw |Us |Ms  ||   |   |   |   |   |   |   |    ||   |   |   |   |   |   |   |    |
        @staticmethod
        def makeSwitchPodcast():
            msg = REDBoxMsg()


            msg.setMsgType(REDBoxMsg.MsgType.MsgType_UserAction)
            msg.setUserAction(REDBoxMsg.UserAction.UserAction_Switch)

            msg.setSwitch(REDBoxMsg.Switch.Switch_Podcast)


            return msg

        # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    |
        # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
        # |   |   |   |Sw |Sw |Sw |Us |Ms  ||   |   |   |   |   |   |   |    ||   |   |   |   |   |   |   |    |
        @staticmethod
        def makeSwitchPrevious():
            msg = REDBoxMsg()


            msg.setMsgType(REDBoxMsg.MsgType.MsgType_UserAction)
            msg.setUserAction(REDBoxMsg.UserAction.UserAction_Switch)

            msg.setSwitch(REDBoxMsg.Switch.Switch_Previous)


            return msg

        # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    |
        # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
        # |   |   |   |Sw |Sw |Sw |Us |Ms  ||   |   |   |   |   |   |   |    ||   |   |   |   |   |   |   |    |
        @staticmethod
        def makeSwitchNext():
            msg = REDBoxMsg()


            msg.setMsgType(REDBoxMsg.MsgType.MsgType_UserAction)
            msg.setUserAction(REDBoxMsg.UserAction.UserAction_Switch)

            msg.setSwitch(REDBoxMsg.Switch.Switch_Next)


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
 



        def processQueryProtocolVersion(self):
            raise NotImplementedError




        def process(self, in_msg):
            if in_msg.getMsgType() == REDBoxMsg.MsgType.MsgType_UserAction:
                pass

            elif in_msg.getMsgType() == REDBoxMsg.MsgType.MsgType_System:
                if in_msg.getSystem() == REDBoxMsg.System.System_QueryProtocolVersion:
                    self.processQueryProtocolVersion()


                elif in_msg.getSystem() == REDBoxMsg.System.System_SendProtocolVersion:
                    pass




