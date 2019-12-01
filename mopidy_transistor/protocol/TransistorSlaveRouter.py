from .TransistorMsg import TransistorMsg


class TransistorSlaveRouter(object):
    # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    ||03 |   |   |   |   |   |   |    |
    # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
    # |   |   |   |Po |Co |Co |Ms |Ms  ||Va |Va |Va |Va |Va |Va |Va |Va  ||Va |Va |Va |Va |Va |Va |Va |Va  ||   |   |   |   |   |   |   |    |
    # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    ||03 |   |   |   |   |   |   |    |
    # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
    # |   |   |   |Po |Co |Co |Ms |Ms  ||Va |Va |Va |Va |Va |Va |Va |Va  ||Va |Va |Va |Va |Va |Va |Va |Va  ||   |   |   |   |   |   |   |    |
    @staticmethod
    def makePotentiometerVolume(in_potentiometervalue):
        msg = TransistorMsg()

        msg.setMsgType(TransistorMsg.MsgType.MsgType_Command)
        msg.setCommand(TransistorMsg.Command.Command_Potentiometer)

        msg.setPotentiometer(TransistorMsg.Potentiometer.Potentiometer_Volume)

        msg.setPotentiometerValue(in_potentiometervalue)

        return msg

    # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    ||03 |   |   |   |   |   |   |    |
    # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
    # |   |   |   |Po |Co |Co |Ms |Ms  ||Va |Va |Va |Va |Va |Va |Va |Va  ||Va |Va |Va |Va |Va |Va |Va |Va  ||   |   |   |   |   |   |   |    |
    @staticmethod
    def makePotentiometerTuner(in_potentiometervalue):
        msg = TransistorMsg()

        msg.setMsgType(TransistorMsg.MsgType.MsgType_Command)
        msg.setCommand(TransistorMsg.Command.Command_Potentiometer)

        msg.setPotentiometer(TransistorMsg.Potentiometer.Potentiometer_Tuner)

        msg.setPotentiometerValue(in_potentiometervalue)

        return msg

    # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    ||03 |   |   |   |   |   |   |    |
    # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
    # |   |   |   |   |Co |Co |Ms |Ms  ||   |   |   |   |   |   |   |    ||   |   |   |   |   |   |   |    ||   |   |   |   |   |   |   |    |
    @staticmethod
    def makePowerOff():
        msg = TransistorMsg()

        msg.setMsgType(TransistorMsg.MsgType.MsgType_Command)
        msg.setCommand(TransistorMsg.Command.Command_PowerOff)

        return msg

    # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    ||03 |   |   |   |   |   |   |    |
    # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
    # |   |   |Ty |Ty |Co |Co |Ms |Ms  ||   |   |   |   |   |   |   |    ||   |   |   |   |   |   |   |    ||   |   |   |   |   |   |   |    |
    @staticmethod
    def makeMode(in_modetype):
        msg = TransistorMsg()

        msg.setMsgType(TransistorMsg.MsgType.MsgType_Command)
        msg.setCommand(TransistorMsg.Command.Command_Mode)

        msg.setModeType(in_modetype)

        return msg

    # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    ||03 |   |   |   |   |   |   |    |
    # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
    # |   |   |   |Ty |Co |Co |Ms |Ms  ||   |   |   |   |   |   |   |    ||   |   |   |   |   |   |   |    ||   |   |   |   |   |   |   |    |
    @staticmethod
    def makeNavigation(in_navigationtype):
        msg = TransistorMsg()

        msg.setMsgType(TransistorMsg.MsgType.MsgType_Command)
        msg.setCommand(TransistorMsg.Command.Command_Navigation)

        msg.setNavigationType(in_navigationtype)

        return msg

    # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    ||03 |   |   |   |   |   |   |    |
    # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
    # |Dd |Dd |Dd |Dd |Dd |Da |Ms |Ms  ||Yy |Yy |Yy |Yy |Yy |Yy |Yy |Yy  ||Mm |Mm |Mm |Mm |Yy |Yy |Yy |Yy  ||   |   |   |   |   |   |   |    |
    @staticmethod
    def makeDate(in_datedate, in_datemonth, in_dateyear):
        msg = TransistorMsg()

        msg.setMsgType(TransistorMsg.MsgType.MsgType_DateTime)
        msg.setDateTime(TransistorMsg.DateTime.DateTime_Date)

        msg.setDateDate(in_datedate)
        msg.setDateMonth(in_datemonth)
        msg.setDateYear(in_dateyear)

        return msg

    # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    ||03 |   |   |   |   |   |   |    |
    # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
    # |Ho |Ho |Ho |Ho |Ho |Da |Ms |Ms  ||Se |Se |Mi |Mi |Mi |Mi |Mi |Mi  ||   |   |   |   |Se |Se |Se |Se  ||   |   |   |   |   |   |   |    |
    @staticmethod
    def makeTime(in_timehour, in_timeminute, in_timesecond):
        msg = TransistorMsg()

        msg.setMsgType(TransistorMsg.MsgType.MsgType_DateTime)
        msg.setDateTime(TransistorMsg.DateTime.DateTime_Time)

        msg.setTimeHour(in_timehour)
        msg.setTimeMinute(in_timeminute)
        msg.setTimeSecond(in_timesecond)

        return msg

    # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    ||03 |   |   |   |   |   |   |    |
    # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
    # |Pc |Pc |Pc |Sy |Sy |Sy |Ms |Ms  ||   |   |   |Pc |Pc |Pc |Pc |Pc  ||   |   |   |   |   |   |   |    ||   |   |   |   |   |   |   |    |
    @staticmethod
    def makeSendBatteryStatus(in_sendbatterystatuspercentage):
        msg = TransistorMsg()

        msg.setMsgType(TransistorMsg.MsgType.MsgType_System)
        msg.setSystem(TransistorMsg.System.System_SendBatteryStatus)

        msg.setSendBatteryStatusPercentage(in_sendbatterystatuspercentage)

        return msg

    # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    ||03 |   |   |   |   |   |   |    |
    # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
    # |Ma |Ma |Ma |Sy |Sy |Sy |Ms |Ms  ||   |   |   |Mi |Mi |Mi |Mi |Ma  ||   |   |   |   |   |   |   |    ||   |   |   |   |   |   |   |    |
    @staticmethod
    def makeSendProtocolVersion(
        in_sendprotocolversionmajor, in_sendprotocolversionminor
    ):
        msg = TransistorMsg()

        msg.setMsgType(TransistorMsg.MsgType.MsgType_System)
        msg.setSystem(TransistorMsg.System.System_SendProtocolVersion)

        msg.setSendProtocolVersionMajor(in_sendprotocolversionmajor)
        msg.setSendProtocolVersionMinor(in_sendprotocolversionminor)

        return msg

    def processQueryProtocolVersion(self):
        raise NotImplementedError

    def processCalibrate(self, in_calibratepotentiometer, in_calibratephase):
        raise NotImplementedError

    def processSaveCalibration(self):
        raise NotImplementedError

    def processSetDate(self, in_setdatedate, in_setdatemonth, in_setdateyear):
        raise NotImplementedError

    def processSetTime(self, in_settimehour, in_settimeminute, in_settimesecond):
        raise NotImplementedError

    def process(self, in_msg):
        if in_msg.getMsgType() == TransistorMsg.MsgType.MsgType_Command:
            pass

        elif in_msg.getMsgType() == TransistorMsg.MsgType.MsgType_DateTime:
            pass

        elif in_msg.getMsgType() == TransistorMsg.MsgType.MsgType_System:
            if in_msg.getSystem() == TransistorMsg.System.System_SendBatteryStatus:
                pass

            elif in_msg.getSystem() == TransistorMsg.System.System_QueryProtocolVersion:
                self.processQueryProtocolVersion()

            elif in_msg.getSystem() == TransistorMsg.System.System_SendProtocolVersion:
                pass

            elif in_msg.getSystem() == TransistorMsg.System.System_Calibrate:
                self.processCalibrate(
                    in_msg.getCalibratePotentiometer(), in_msg.getCalibratePhase()
                )

            elif in_msg.getSystem() == TransistorMsg.System.System_SaveCalibration:
                self.processSaveCalibration()

            elif in_msg.getSystem() == TransistorMsg.System.System_SetDateTime:
                if (
                    in_msg.getSetDateTime()
                    == TransistorMsg.SetDateTime.SetDateTime_SetDate
                ):
                    self.processSetDate(
                        in_msg.getSetDateDate(),
                        in_msg.getSetDateMonth(),
                        in_msg.getSetDateYear(),
                    )

                elif (
                    in_msg.getSetDateTime()
                    == TransistorMsg.SetDateTime.SetDateTime_SetTime
                ):
                    self.processSetTime(
                        in_msg.getSetTimeHour(),
                        in_msg.getSetTimeMinute(),
                        in_msg.getSetTimeSecond(),
                    )
