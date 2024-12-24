# Python Imports
from typing import Any

# FRC Imports
from wpilib import RobotController, RobotBase
from ntcore import NetworkTableInstance, NetworkTable, StructPublisher, _setNow

class FalconLogger:
    __outputBase:str = "Real"
    __tbl:NetworkTable = NetworkTableInstance.getDefault().getTable("/")
    __publishers:dict = {}
    __inputs:dict = {}
    __outputs:dict = {}

    def __init__(self, isReplay:bool = False) -> None:
        if RobotBase.isSimulation():
            if isReplay:
                self.__outputBase = "Replay"
            else:
                self.__outputBase = "Sim"

    def setTime(self) -> None:
        _setNow( RobotController.getFPGATime() )

    def writeLog(self) -> None:
        self.__writeLog( "Logging", self.__inputs )
        self.__writeLog( f"{self.__outputBase}Outputs", self.__outputs )     

    def __writeLog(self, key:str, logData:dict) -> None:
        # Loop Through Records Currently In the Log Data
        # Commit Logs to Network Tables
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

    @classmethod
    def logInput(self, key:str, value:Any) -> None:
        self.__inputs.update({ key: value })

    @classmethod
    def logOutput(self, key:str, value:Any) -> None:
        self.__outputs.update( {key: value} )
