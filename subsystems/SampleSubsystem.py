from commands2 import Subsystem
from wpilib import RobotState
from ntcore import NetworkTable, NetworkTableInstance

class SampleSubsystem(Subsystem):
    # Variable Declaration
    m_value:float = 0.0
    m_system:int = None
    m_logging:NetworkTable = None

    # Initialization
    def __init__(self, sysId:int) -> None:
        self.m_system = sysId
        self.m_value = 0.0
        self.m_logging = NetworkTableInstance.getDefault().getTable("/Logging/SampleSubsystem")

    # Periodic Loop
    def periodic(self) -> None:
        # Logging: Write Current Subsystem State
        self.m_logging.putNumber( "SubsystemData", 0.0 )

        # Run Subsystem: Set New State To Subsystem
        if RobotState.isDisabled():
            self.stop()
        else:
            self.run()
        
        # Logging: Write Post Operation Information
        self.m_logging.putNumber( "Setpoint", self.getSetpoint() )
        self.m_logging.putNumber( "Measured", self.m_system )

    # Run the Subsystem
    def run(self) -> None:
        pass

    # Stop the Subsystem
    def stop(self) -> None:
        pass

    # Set the Desired State Value
    def setSetpoint(self, value:float) -> None:
        self.m_value = value

    # Get the Desired State Value
    def getSetpoint(self) -> float:
        return self.m_value
    
    # Check if Subsystem is at the Desired State
    def atSetpoint(self) -> bool:
        return False