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
    # |   |   |   |   |   |   |   |Ms  ||   |   |   |   |   |   |   |    ||   |   |   |   |   |   |   |    |
    class MsgType(Enum):
        MsgType_UserAction = 0
        MsgType_System = 1
    def getMsgType(self):
        return REDBoxMsg.MsgType( self.get(0, 1)  )
    def setMsgType(self, in_msgtype):
        self.set(0, 1, in_msgtype.value)
        
    # UserAction
    # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    |
    # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
    # |   |   |   |   |   |   |Us |    ||   |   |   |   |   |   |   |    ||   |   |   |   |   |   |   |    |
    class UserAction(Enum):
        UserAction_Potentiometer = 0
        UserAction_Switch = 1
    def getUserAction(self):
        return REDBoxMsg.UserAction( self.get(1, 1)  )
    def setUserAction(self, in_useraction):
        self.set(1, 1, in_useraction.value)
        
    # Potentiometer
    # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    |
    # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
    # |   |   |   |   |   |Po |   |    ||   |   |   |   |   |   |   |    ||   |   |   |   |   |   |   |    |
    class Potentiometer(Enum):
        Potentiometer_Volume = 0
        Potentiometer_Tuner = 1
    def getPotentiometer(self):
        return REDBoxMsg.Potentiometer( self.get(2, 1)  )
    def setPotentiometer(self, in_potentiometer):
        self.set(2, 1, in_potentiometer.value)
        
    # PotentiometerValue
    # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    |
    # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
    # |   |   |   |   |   |   |   |    ||Va |Va |Va |Va |Va |Va |Va |Va  ||Va |Va |Va |Va |Va |Va |Va |Va  |
    def getPotentiometerValue(self):
        return self.get(8, 16)
    def setPotentiometerValue(self, in_potentiometervalue):
        self.set(8, 16, in_potentiometervalue)
        
    # Switch
    # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    |
    # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
    # |   |   |   |Sw |Sw |Sw |   |    ||   |   |   |   |   |   |   |    ||   |   |   |   |   |   |   |    |
    class Switch(Enum):
        Switch_Power = 0
        Switch_Radio = 1
        Switch_Podcast = 2
        Switch_Previous = 3
        Switch_Next = 4
    def getSwitch(self):
        return REDBoxMsg.Switch( self.get(2, 3)  )
    def setSwitch(self, in_switch):
        self.set(2, 3, in_switch.value)
        
    # System
    # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    |
    # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
    # |   |   |   |   |   |   |Sy |    ||   |   |   |   |   |   |   |    ||   |   |   |   |   |   |   |    |
    class System(Enum):
        System_QueryProtocolVersion = 0
        System_SendProtocolVersion = 1
    def getSystem(self):
        return REDBoxMsg.System( self.get(1, 1)  )
    def setSystem(self, in_system):
        self.set(1, 1, in_system.value)
        
    # SendProtocolVersionMajor
    # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    |
    # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
    # |   |   |Ma |Ma |Ma |Ma |   |    ||   |   |   |   |   |   |   |    ||   |   |   |   |   |   |   |    |
    def getSendProtocolVersionMajor(self):
        return self.get(2, 4)
    def setSendProtocolVersionMajor(self, in_sendprotocolversionmajor):
        self.set(2, 4, in_sendprotocolversionmajor)
        
    # SendProtocolVersionMinor
    # |00 |   |   |   |   |   |   |    ||01 |   |   |   |   |   |   |    ||02 |   |   |   |   |   |   |    |
    # |07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  ||07 |06 |05 |04 |03 |02 |01 |00  |
    # |Mi |Mi |   |   |   |   |   |    ||   |   |   |   |   |   |Mi |Mi  ||   |   |   |   |   |   |   |    |
    def getSendProtocolVersionMinor(self):
        return self.get(6, 4)
    def setSendProtocolVersionMinor(self, in_sendprotocolversionminor):
        self.set(6, 4, in_sendprotocolversionminor)
        
