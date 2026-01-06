from commands2 import Subsystem
from wpilib import RobotState
from ntcore import NetworkTable, NetworkTableInstance

class ExampleSubsystem(Subsystem):
    # Variable Type Declaration
    value:float = 0.0
    system:int = None
    logging:NetworkTable = None

    def __init__(self, sysId:int) -> None:
        self.system = sysId
        self.value = 0.0
        self.logging = NetworkTableInstance.getDefault().getTable("/Logging/ExampleSubsystem")

    def periodic(self) -> None:
        # Logging: Write Current Subsystem State
        self.logging.putNumber( "SubsystemData", 0.0 )

        # Run Subsystem: Set New State To Subsystem
        if RobotState.isDisabled():
            self.stop()
        else:
            self.run()
        
        # Logging: Write Post Operation Information
        self.logging.putNumber( "Setpoint", self.getSetpoint() )
        self.logging.putNumber( "Measured", self.system )

    def run(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def setSetpoint(self, value:float) -> None:
        """
        Set Desired State value
        """
        self.value = value

    def getSetpoint(self) -> float:
        """
        Get Desired State value
        """
        return self.value
    
    def atSetpoint(self) -> bool:
        return False