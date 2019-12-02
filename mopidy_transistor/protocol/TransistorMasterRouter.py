from .TransistorMsg import TransistorMsg


class TransistorMasterRouter(object):
    # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    ||03 |   |   |   |   |   |   |    |
    # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
    # |   |   |   |Sy |Sy |Sy |Ms |Ms  ||   |   |   |   |   |   |   |    ||   |   |   |   |   |   |   |    ||   |   |   |   |   |   |   |    |
    @staticmethod
    def makeQueryProtocolVersion():
        msg = TransistorMsg()

        msg.setMsgType(TransistorMsg.MsgType.MsgType_System)
        msg.setSystem(TransistorMsg.System.System_QueryProtocolVersion)

        return msg

    # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    ||03 |   |   |   |   |   |   |    |
    # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
    # |Ph |Ph |Po |Sy |Sy |Sy |Ms |Ms  ||   |   |   |   |   |   |   |    ||   |   |   |   |   |   |   |    ||   |   |   |   |   |   |   |    |
    @staticmethod
    def makeCalibrate(in_calibratepotentiometer, in_calibratephase):
        msg = TransistorMsg()

        msg.setMsgType(TransistorMsg.MsgType.MsgType_System)
        msg.setSystem(TransistorMsg.System.System_Calibrate)

        msg.setCalibratePotentiometer(in_calibratepotentiometer)
        msg.setCalibratePhase(in_calibratephase)

        return msg

    # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    ||03 |   |   |   |   |   |   |    |
    # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
    # |   |   |   |Sy |Sy |Sy |Ms |Ms  ||   |   |   |   |   |   |   |    ||   |   |   |   |   |   |   |    ||   |   |   |   |   |   |   |    |
    @staticmethod
    def makeSaveCalibration():
        msg = TransistorMsg()

        msg.setMsgType(TransistorMsg.MsgType.MsgType_System)
        msg.setSystem(TransistorMsg.System.System_SaveCalibration)

        return msg

    # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    ||03 |   |   |   |   |   |   |    |
    # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
    # |   |   |Se |Sy |Sy |Sy |Ms |Ms  ||Yy |Yy |Yy |Yy |Yy |Yy |Yy |Yy  ||Dd |Dd |Dd |Dd |Yy |Yy |Yy |Yy  ||   |   |   |Mm |Mm |Mm |Mm |Dd  |
    @staticmethod
    def makeSetDate(in_setdatedate, in_setdatemonth, in_setdateyear):
        msg = TransistorMsg()

        msg.setMsgType(TransistorMsg.MsgType.MsgType_System)
        msg.setSystem(TransistorMsg.System.System_SetDateTime)
        msg.setSetDateTime(TransistorMsg.SetDateTime.SetDateTime_SetDate)

        msg.setSetDateDate(in_setdatedate)
        msg.setSetDateMonth(in_setdatemonth)
        msg.setSetDateYear(in_setdateyear)

        return msg

    # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    ||03 |   |   |   |   |   |   |    |
    # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
    # |Ho |Ho |Se |Sy |Sy |Sy |Ms |Ms  ||Mi |Mi |Mi |Mi |Mi |Ho |Ho |Ho  ||   |Se |Se |Se |Se |Se |Se |Mi  ||   |   |   |   |   |   |   |    |
    @staticmethod
    def makeSetTime(in_settimehour, in_settimeminute, in_settimesecond):
        msg = TransistorMsg()

        msg.setMsgType(TransistorMsg.MsgType.MsgType_System)
        msg.setSystem(TransistorMsg.System.System_SetDateTime)
        msg.setSetDateTime(TransistorMsg.SetDateTime.SetDateTime_SetTime)

        msg.setSetTimeHour(in_settimehour)
        msg.setSetTimeMinute(in_settimeminute)
        msg.setSetTimeSecond(in_settimesecond)

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

    def processDate(self, in_datedate, in_datemonth, in_dateyear):
        raise NotImplementedError

    def processTime(self, in_timehour, in_timeminute, in_timesecond):
        raise NotImplementedError

    def processSendBatteryStatus(self, in_sendbatterystatuspercentage):
        raise NotImplementedError

    def processSendProtocolVersion(
        self, in_sendprotocolversionmajor, in_sendprotocolversionminor
    ):
        raise NotImplementedError

    def process(self, in_msg):
        if in_msg.getMsgType() == TransistorMsg.MsgType.MsgType_Command:
            if in_msg.getCommand() == TransistorMsg.Command.Command_Potentiometer:
                if (
                    in_msg.getPotentiometer()
                    == TransistorMsg.Potentiometer.Potentiometer_Volume
                ):
                    self.processPotentiometerVolume(in_msg.getPotentiometerValue())
                elif (
                    in_msg.getPotentiometer()
                    == TransistorMsg.Potentiometer.Potentiometer_Tuner
                ):
                    self.processPotentiometerTuner(in_msg.getPotentiometerValue())

            elif in_msg.getCommand() == TransistorMsg.Command.Command_PowerOff:
                self.processPowerOff()

            elif in_msg.getCommand() == TransistorMsg.Command.Command_Mode:
                self.processMode(in_msg.getModeType())

            elif in_msg.getCommand() == TransistorMsg.Command.Command_Navigation:
                self.processNavigation(in_msg.getNavigationType())

        elif in_msg.getMsgType() == TransistorMsg.MsgType.MsgType_DateTime:
            if in_msg.getDateTime() == TransistorMsg.DateTime.DateTime_Date:
                self.processDate(
                    in_msg.getDateDate(), in_msg.getDateMonth(), in_msg.getDateYear()
                )

            elif in_msg.getDateTime() == TransistorMsg.DateTime.DateTime_Time:
                self.processTime(
                    in_msg.getTimeHour(), in_msg.getTimeMinute(), in_msg.getTimeSecond()
                )

        elif in_msg.getMsgType() == TransistorMsg.MsgType.MsgType_System:
            if in_msg.getSystem() == TransistorMsg.System.System_SendBatteryStatus:
                self.processSendBatteryStatus(in_msg.getSendBatteryStatusPercentage())

            elif in_msg.getSystem() == TransistorMsg.System.System_QueryProtocolVersion:
                pass

            elif in_msg.getSystem() == TransistorMsg.System.System_SendProtocolVersion:
                self.processSendProtocolVersion(
                    in_msg.getSendProtocolVersionMajor(),
                    in_msg.getSendProtocolVersionMinor(),
                )

            elif in_msg.getSystem() == TransistorMsg.System.System_Calibrate:
                pass

            elif in_msg.getSystem() == TransistorMsg.System.System_SaveCalibration:
                pass

            elif in_msg.getSystem() == TransistorMsg.System.System_SetDateTime:
                pass
