# Python Imports
from enum import Enum, auto

# FRC Imports
from wpilib import SendableChooser, SmartDashboard
from commands2 import Command, cmd

# Local Imports
from subsystems import ExampleSubsystem
from commands import ExampleCommand
from util import FalconXboxController

class ControlMode(Enum):
    TEST = auto()
    PRACTICE = auto()
    COMP = auto()
    DEMO = auto()
    

class RobotContainer:
    """
    RobotContainer is the Initial Container for an FRC Robot
    """
    __autoChooser:SendableChooser = SendableChooser()

    def __init__(self):
        """
        Initializes RobotContainer
        """
        ## Config
        control_mode = ControlMode.TEST

        # Driver Controller
        driver1 = FalconXboxController( 0 )

        # Declare Subsystems
        sysSample = ExampleSubsystem( 0 )

        # Commands
        cmdSampleLeft = ExampleCommand(sysSample, driver1.getLeftX )
        cmdSampleRight = ExampleCommand(sysSample, driver1.getRightX )

        # Default Commands
        sysSample.setDefaultCommand( cmdSampleLeft )

        # Autonomous Chooser
        self.__autoChooser.setDefaultOption( "1 - None", cmd.none() )
        SmartDashboard.putData( "Autonomous Mode", self.__autoChooser )

        ## Setup Controls
        match control_mode:
            case ControlMode.TEST:
                self.setControlsTest()
            case ControlMode.PRACTICE:
                self.setControlsPractice()
            case ControlMode.COMP:
                self.setControlsComp()
            case ControlMode.DEMO:
                self.setControlsDemo()

    def setControlsTest(self):
        pass
    def setControlsPractice(self):
        pass
    def setControlsComp(self):
        pass
    def setControlsDemo(self):
        pass

    def getAutonomousCommand(self) -> Command:
        """
        Get the Autonomous Command that is currently selected in the AutoChooser Dropdown on the Shuffleboard / SmartDashboards
        """
        chooserValue = self.__autoChooser.getSelected()
        return chooserValue if isinstance( chooserValue, Command ) else cmd.none()
