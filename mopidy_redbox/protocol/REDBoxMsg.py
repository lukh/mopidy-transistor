from enum import Enum
import microparcel as mp

class REDBoxMsg(mp.Message):
    PROTOCOL_VERSION_MAJOR = 1
    PROTOCOL_VERSION_MINOR = 0

    def __init__(self):
        super(REDBoxMsg, self).__init__(size=3)

    # --- Common enums ---

    # --- Common fields ---


    # --- Message fields ---
    # MsgType
    # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    |
    # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
    # |   |   |   |   |   |   |Ms |Ms  ||   |   |   |   |   |   |   |    ||   |   |   |   |   |   |   |    |
    class MsgType(Enum):
        MsgType_Command = 0
        MsgType_DateTime = 1
        MsgType_System = 2
    def getMsgType(self):
        return REDBoxMsg.MsgType( self.get(0, 2)  )
    def setMsgType(self, in_msgtype):
        self.set(0, 2, in_msgtype.value)
        
    # Command
    # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    |
    # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
    # |   |   |   |   |Co |Co |   |    ||   |   |   |   |   |   |   |    ||   |   |   |   |   |   |   |    |
    class Command(Enum):
        Command_Potentiometer = 0
        Command_PowerOff = 1
        Command_Mode = 2
        Command_Navigation = 3
    def getCommand(self):
        return REDBoxMsg.Command( self.get(2, 2)  )
    def setCommand(self, in_command):
        self.set(2, 2, in_command.value)
        
    # Potentiometer
    # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    |
    # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
    # |   |   |   |Po |   |   |   |    ||   |   |   |   |   |   |   |    ||   |   |   |   |   |   |   |    |
    class Potentiometer(Enum):
        Potentiometer_Volume = 0
        Potentiometer_Tuner = 1
    def getPotentiometer(self):
        return REDBoxMsg.Potentiometer( self.get(4, 1)  )
    def setPotentiometer(self, in_potentiometer):
        self.set(4, 1, in_potentiometer.value)
        
    # PotentiometerValue
    # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    |
    # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
    # |   |   |   |   |   |   |   |    ||Va |Va |Va |Va |Va |Va |Va |Va  ||Va |Va |Va |Va |Va |Va |Va |Va  |
    def getPotentiometerValue(self):
        return self.get(8, 16)
    def setPotentiometerValue(self, in_potentiometervalue):
        self.set(8, 16, in_potentiometervalue)
        
    # ModeType
    # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    |
    # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
    # |   |   |Ty |Ty |   |   |   |    ||   |   |   |   |   |   |   |    ||   |   |   |   |   |   |   |    |
    class ModeType(Enum):
        ModeType_NextMode = 0
        ModeType_Radio = 1
        ModeType_Podcast = 2
    def getModeType(self):
        return REDBoxMsg.ModeType( self.get(4, 2)  )
    def setModeType(self, in_modetype):
        self.set(4, 2, in_modetype.value)
        
    # NavigationType
    # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    |
    # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
    # |   |   |   |Ty |   |   |   |    ||   |   |   |   |   |   |   |    ||   |   |   |   |   |   |   |    |
    class NavigationType(Enum):
        NavigationType_Previous = 0
        NavigationType_Next = 1
    def getNavigationType(self):
        return REDBoxMsg.NavigationType( self.get(4, 1)  )
    def setNavigationType(self, in_navigationtype):
        self.set(4, 1, in_navigationtype.value)
        
    # DateTime
    # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    |
    # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
    # |   |   |   |   |   |Da |   |    ||   |   |   |   |   |   |   |    ||   |   |   |   |   |   |   |    |
    class DateTime(Enum):
        DateTime_Date = 0
        DateTime_Time = 1
    def getDateTime(self):
        return REDBoxMsg.DateTime( self.get(2, 1)  )
    def setDateTime(self, in_datetime):
        self.set(2, 1, in_datetime.value)
        
    # DateDay
    # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    |
    # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
    # |   |   |Dd |Dd |Dd |   |   |    ||   |   |   |   |   |   |   |    ||   |   |   |   |   |   |   |    |
    def getDateDay(self):
        return self.get(3, 3)
    def setDateDay(self, in_dateday):
        self.set(3, 3, in_dateday)
        
    # DateMonth
    # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    |
    # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
    # |   |   |   |   |   |   |   |    ||   |   |   |   |   |   |   |    ||Mm |Mm |Mm |Mm |   |   |   |    |
    def getDateMonth(self):
        return self.get(20, 4)
    def setDateMonth(self, in_datemonth):
        self.set(20, 4, in_datemonth)
        
    # DateYear
    # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    |
    # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
    # |   |   |   |   |   |   |   |    ||Yy |Yy |Yy |Yy |Yy |Yy |Yy |Yy  ||   |   |   |   |Yy |Yy |Yy |Yy  |
    def getDateYear(self):
        return self.get(8, 12)
    def setDateYear(self, in_dateyear):
        self.set(8, 12, in_dateyear)
        
    # TimeHour
    # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    |
    # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
    # |Ho |Ho |Ho |Ho |Ho |   |   |    ||   |   |   |   |   |   |   |    ||   |   |   |   |   |   |   |    |
    def getTimeHour(self):
        return self.get(3, 5)
    def setTimeHour(self, in_timehour):
        self.set(3, 5, in_timehour)
        
    # TimeMinute
    # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    |
    # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
    # |   |   |   |   |   |   |   |    ||   |   |Mi |Mi |Mi |Mi |Mi |Mi  ||   |   |   |   |   |   |   |    |
    def getTimeMinute(self):
        return self.get(8, 6)
    def setTimeMinute(self, in_timeminute):
        self.set(8, 6, in_timeminute)
        
    # TimeSecond
    # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    |
    # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
    # |   |   |   |   |   |   |   |    ||Se |Se |   |   |   |   |   |    ||   |   |   |   |Se |Se |Se |Se  |
    def getTimeSecond(self):
        return self.get(14, 6)
    def setTimeSecond(self, in_timesecond):
        self.set(14, 6, in_timesecond)
        
    # System
    # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    |
    # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
    # |   |   |   |Sy |Sy |Sy |   |    ||   |   |   |   |   |   |   |    ||   |   |   |   |   |   |   |    |
    class System(Enum):
        System_SendBatteryStatus = 0
        System_QueryProtocolVersion = 1
        System_SendProtocolVersion = 2
        System_Calibrate = 3
        System_SaveCalibration = 4
    def getSystem(self):
        return REDBoxMsg.System( self.get(2, 3)  )
    def setSystem(self, in_system):
        self.set(2, 3, in_system.value)
        
    # SendBatteryStatusPercentage
    # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    |
    # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
    # |Pc |Pc |Pc |   |   |   |   |    ||   |   |   |Pc |Pc |Pc |Pc |Pc  ||   |   |   |   |   |   |   |    |
    def getSendBatteryStatusPercentage(self):
        return self.get(5, 8)
    def setSendBatteryStatusPercentage(self, in_sendbatterystatuspercentage):
        self.set(5, 8, in_sendbatterystatuspercentage)
        
    # SendProtocolVersionMajor
    # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    |
    # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
    # |Ma |Ma |Ma |   |   |   |   |    ||   |   |   |   |   |   |   |Ma  ||   |   |   |   |   |   |   |    |
    def getSendProtocolVersionMajor(self):
        return self.get(5, 4)
    def setSendProtocolVersionMajor(self, in_sendprotocolversionmajor):
        self.set(5, 4, in_sendprotocolversionmajor)
        
    # SendProtocolVersionMinor
    # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    |
    # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
    # |   |   |   |   |   |   |   |    ||   |   |   |Mi |Mi |Mi |Mi |    ||   |   |   |   |   |   |   |    |
    def getSendProtocolVersionMinor(self):
        return self.get(9, 4)
    def setSendProtocolVersionMinor(self, in_sendprotocolversionminor):
        self.set(9, 4, in_sendprotocolversionminor)
        
    # CalibratePotentiometer
    # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    |
    # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
    # |   |   |Po |   |   |   |   |    ||   |   |   |   |   |   |   |    ||   |   |   |   |   |   |   |    |
    class CalibratePotentiometer(Enum):
        CalibratePotentiometer_Volume = 0
        CalibratePotentiometer_Tuner = 1
    def getCalibratePotentiometer(self):
        return REDBoxMsg.CalibratePotentiometer( self.get(5, 1)  )
    def setCalibratePotentiometer(self, in_calibratepotentiometer):
        self.set(5, 1, in_calibratepotentiometer.value)
        
    # CalibratePhase
    # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    |
    # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
    # |Ph |Ph |   |   |   |   |   |    ||   |   |   |   |   |   |   |    ||   |   |   |   |   |   |   |    |
    class CalibratePhase(Enum):
        CalibratePhase_StartLow = 0
        CalibratePhase_StopLow = 1
        CalibratePhase_StartHigh = 2
        CalibratePhase_StopHigh = 3
    def getCalibratePhase(self):
        return REDBoxMsg.CalibratePhase( self.get(6, 2)  )
    def setCalibratePhase(self, in_calibratephase):
        self.set(6, 2, in_calibratephase.value)
        
