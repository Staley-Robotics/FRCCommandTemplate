from commands2 import Subsystem
from wpilib import RobotState
from ntcore import NetworkTable, NetworkTableInstance

from util import FalconLogger

class ExampleSubsystem(Subsystem):
    def __init__(self, value1:int) -> None:
        """
        Initialize Subsystem
        Called when the subsystem is created
        """
        self.value1 = value1
        self.value2 = 0.0

    def periodic(self) -> None:
        # Logging: Write Current Subsystem State
        FalconLogger.logInput( "/ExampleSubsystem/exampleMeasurement", 0.0 )

        # Run Subsystem: Set New State To Subsystem
        if RobotState.isDisabled():
            self.stop()
        else:
            self.run()
        
        # Logging: Write Post Operation Information
        FalconLogger.logOutput( "/ExampleSubsystem/setpoint", self.getSetpoint() )

    def run(self) -> None:
        ... # apply motor controls

    def stop(self) -> None:
        ... # force motor stop behavior

    def setSetpoint(self, value:float) -> None:
        """
        Set Desired State value
        NOTE: in a real subsystem, try to use a specific term like 'setSpeed' or 'setDesiredPosition', 'setSetPosition' would also be acceptable, but is less readable
        - make sure to use 'Desired' or 'Set' when using closed-loop control to avoid confusion
        """
        self.value2 = value

    def getSetpoint(self) -> float:
        """
        Get Desired State value
        """
        return self.value2
    
    def atSetpoint(self) -> bool:
        """
        Get whether or not the subsystem is at it's setpoint
        """
        return False