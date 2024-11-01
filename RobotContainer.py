from commands2 import Command
from commands2.button import CommandXboxController
import commands2.cmd as cmd
from wpilib import SendableChooser, SmartDashboard

from commands.SampleCommand import SampleCommand
from subsystems.SampleSubsystem import SampleSubsystem

class RobotContainer:
    # Variable Declaration
    m_autoChooser:SendableChooser = None

    # Initialization
    def __init__(self):
        # Driver Controller
        self.m_driver1 = CommandXboxController( 0 )

        # Declare Subsystems
        self.m_subsys = SampleSubsystem( 0 )

        # Commands
        self.leftX = SampleCommand(self.m_subsys, self.m_driver1.getLeftX )
        self.rightX = SampleCommand(self.m_subsys, self.m_driver1.getRightX )

        # Autonomous Chooser
        self.m_autoChooser = SendableChooser()
        self.m_autoChooser.setDefaultOption( "1 - None", cmd.none() )
        SmartDashboard.putData( "Autonomous Mode", self.m_autoChooser )

        # Default Commands
        self.m_subsys.setDefaultCommand( self.leftX )

        # Driver Controller Button Binding
        self.m_driver1.a().whileTrue( self.rightX )

    # Get Autonomous Command
    def getAutonomousCommand(self) -> Command:
        chooserValue = self.m_autoChooser.getSelected()
        if type(chooserValue) == Command:
            return chooserValue
        else:
            return cmd.none()