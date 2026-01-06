# Python Imports
from typing import Any

# FRC Imports
from wpilib import RobotController, RobotBase
from ntcore import NetworkTableInstance, NetworkTable, StructPublisher, _setNow

from rev import SparkMax

class FalconLogger:
    __outputBase:str = "Real"
    __tbl:NetworkTable = NetworkTableInstance.getDefault().getTable("/")
    __publishers:dict = {}
    __inputs:dict = {}
    __outputs:dict = {}
    __LOGGABLE_OBJECTS:set[type] = {SparkMax}
    __logged_objects:dict = {}

    def __init__(self, isReplay:bool = False) -> None:
        if RobotBase.isSimulation():
            if isReplay:
                self.__outputBase = "Replay"
            else:
                self.__outputBase = "Sim"

    def setTime(self) -> None:
        _setNow( RobotController.getFPGATime() )

    def writeLog(self) -> None:
        """
        Commits all cached logs to NetworkTables
        """
        self.__readLoggedObjectsToInputs()

        self.__writeLog( "Logging", self.__inputs )
        self.__writeLog( f"{self.__outputBase}Outputs", self.__outputs )     

    def __writeLog(self, key:str, logData:dict) -> None:
        """
        Loop Through Records Currently In the Log Data
        Commit Logs to Network Tables
        """
        for k, v in logData.items():
            path = f"{key}/{k}"
            match v:
                case list():
                    match v[0]:
                        case bool():
                            self.__tbl.putBooleanArray( path, v )
                        case str():
                            self.__tbl.putStringArray( path, v )
                        case float() | int():
                            self.__tbl.putNumberArray( path, v )
                        case _:
                            if v[0].WPIStruct != None:
                                if path not in self.__publishers:
                                    self.__publishers.update( {path: self.__tbl.getStructArrayTopic( path, type(v[0]) ).publish() } )
                                pub:StructPublisher = self.__publishers[path]
                                pub.set( v )
                            else:
                                print( f"Other type: {type(v)} => {path}: {v}" )
                case bool():
                    self.__tbl.putBoolean( path, v )
                case str():
                    self.__tbl.putString( path, v )
                case float() | int():
                    self.__tbl.putNumber( path, v )
                case _:
                    if v.WPIStruct != None:
                        if path not in self.__publishers:
                            self.__publishers.update( {path: self.__tbl.getStructTopic( path, type(v) ).publish() } )
                        pub:StructPublisher = self.__publishers[path]
                        pub.set( v )
                    else:
                        print( f"Other type: {type(v)} => {path}: {v}" )
        
        # Clear the Log Data Cache
        logData.clear()
    
    def __readLoggedObjectsToInputs(self) -> None:
        """
        reads current data from all logged objects and adds to self.__inputs
        """
        for key, obj in self.__logged_objects.items():
            match obj:
                case SparkMax():
                    self.logInput(f"{key}/MotorInput", obj.get()) # current speed of motor
                    self.logInput(f"{key}/MotorOutput", obj.getAppliedOutput())
                    self.logInput(f"{key}/MotorPosition_r", obj.getPosition())
                    self.logInput(f"{key}/MotorVelocity_rpm", obj.getVelocity())
                    self.logInput(f"{key}/MotorCurrent_a", obj.getOutputCurrent())
                    self.logInput(f"{key}/MotorTemp_c", obj.getMotorTemperature())
                case _:
                    raise TypeError(f"Object of type {type(obj)} was added to LoggedObjects, but has not been implemented")
    
    @classmethod
    def addLoggedObject(self, key:str, value:Any) -> None:
        """
        add or update an object to log its hardware inputs

        :param obj: must be a supported object type.
        currently supported types:
            - SparkMax
        """
        if type(value) not in self.__LOGGABLE_OBJECTS:
            raise TypeError(f"'{type(value)}' is not a supported type for automatic logging, either log its contents manually or implement yourself it in FalconLogger")
        self.__logged_objects.update({ key: value })

    @classmethod
    def logInput(self, key:str, value:Any) -> None:
        """
        add or update a data input to be logged

        should be used exclusively for raw data from hardware inputs
        """
        self.__inputs.update({ key: value })

    @classmethod
    def logOutput(self, key:str, value:Any) -> None:
        """
        add or update a data output to be logged

        should be used exclusively for calculated values
        """
        self.__outputs.update( {key: value} )
