from .REDBoxMsg import REDBoxMsg

class REDBoxMasterRouter(object):
        # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    |
        # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
        # |   |   |   |   |Sy |Sy |Sy |Ms  ||   |   |   |   |   |   |   |    ||   |   |   |   |   |   |   |    |
        @staticmethod
        def makeQueryProtocolVersion():
            msg = REDBoxMsg()


            msg.setMsgType(REDBoxMsg.MsgType.MsgType_System)
            msg.setSystem(REDBoxMsg.System.System_QueryProtocolVersion)


            return msg
 

        # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    |
        # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
        # |   |Ph |Ph |Po |Sy |Sy |Sy |Ms  ||   |   |   |   |   |   |   |    ||   |   |   |   |   |   |   |    |
        @staticmethod
        def makeCalibrate(in_calibratepotentiometer, in_calibratephase):
            msg = REDBoxMsg()


            msg.setMsgType(REDBoxMsg.MsgType.MsgType_System)
            msg.setSystem(REDBoxMsg.System.System_Calibrate)

            msg.setCalibratePotentiometer(in_calibratepotentiometer)
            msg.setCalibratePhase(in_calibratephase)

            return msg
 

        # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    |
        # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
        # |   |   |   |   |Sy |Sy |Sy |Ms  ||   |   |   |   |   |   |   |    ||   |   |   |   |   |   |   |    |
        @staticmethod
        def makeSaveCalibration():
            msg = REDBoxMsg()


            msg.setMsgType(REDBoxMsg.MsgType.MsgType_System)
            msg.setSystem(REDBoxMsg.System.System_SaveCalibration)


            return msg
 



        def processPotentiometerVolume(self, in_potentiometervalue):
            raise NotImplementedError

        def processPotentiometerTuner(self, in_potentiometervalue):
            raise NotImplementedError


        def processPowerOff(self):
            raise NotImplementedError

        def processMode(self, in_modetype):
            raise NotImplementedError

        def processNavigation(self, in_navigationtype):
            raise NotImplementedError

        def processSendBatteryStatus(self, in_sendbatterystatuspercentage):
            raise NotImplementedError

        def processSendProtocolVersion(self, in_sendprotocolversionmajor, in_sendprotocolversionminor):
            raise NotImplementedError




        def process(self, in_msg):
            if in_msg.getMsgType() == REDBoxMsg.MsgType.MsgType_Command:
                if in_msg.getCommand() == REDBoxMsg.Command.Command_Potentiometer:
                    if in_msg.getPotentiometer() == REDBoxMsg.Potentiometer.Potentiometer_Volume:
                        self.processPotentiometerVolume(in_msg.getPotentiometerValue())
                    elif in_msg.getPotentiometer() == REDBoxMsg.Potentiometer.Potentiometer_Tuner:
                        self.processPotentiometerTuner(in_msg.getPotentiometerValue())


                elif in_msg.getCommand() == REDBoxMsg.Command.Command_PowerOff:
                    self.processPowerOff()


                elif in_msg.getCommand() == REDBoxMsg.Command.Command_Mode:
                    self.processMode(in_msg.getModeType())


                elif in_msg.getCommand() == REDBoxMsg.Command.Command_Navigation:
                    self.processNavigation(in_msg.getNavigationType())




            elif in_msg.getMsgType() == REDBoxMsg.MsgType.MsgType_System:
                if in_msg.getSystem() == REDBoxMsg.System.System_SendBatteryStatus:
                    self.processSendBatteryStatus(in_msg.getSendBatteryStatusPercentage())


                elif in_msg.getSystem() == REDBoxMsg.System.System_QueryProtocolVersion:
                    pass

                elif in_msg.getSystem() == REDBoxMsg.System.System_SendProtocolVersion:
                    self.processSendProtocolVersion(in_msg.getSendProtocolVersionMajor(), in_msg.getSendProtocolVersionMinor())


                elif in_msg.getSystem() == REDBoxMsg.System.System_Calibrate:
                    pass

                elif in_msg.getSystem() == REDBoxMsg.System.System_SaveCalibration:
                    pass




