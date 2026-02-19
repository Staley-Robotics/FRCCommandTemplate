from commands2 import Subsystem
from wpilib import RobotState
from ntcore import NetworkTable, NetworkTableInstance

from util import FalconLogger

class ExampleSubsystem(Subsystem):
    # Variable Type Declaration
    value:float = 0.0
    system:int = None

    def __init__(self, sysId:int) -> None:
        self.system = sysId
        self.value = 0.0

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
        pass

    def stop(self) -> None:
        pass

    def setSetpoint(self, value:float) -> None:
        """
        Set Desired State value
        NOTE: in a real subsystem, try to use a specific term like 'setSpeed' or 'setDesiredPosition', 'setSetPosition' would also be acceptable, but is less readable
        - make sure to use 'Desired' or 'Set' when using closed-loop control to avoid confusion
        """
        self.value = value

    def getSetpoint(self) -> float:
        """
        Get Desired State value
        """
        return self.value
    
    def atSetpoint(self) -> bool:
        return False