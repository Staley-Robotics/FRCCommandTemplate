from wpilib import TimedRobot
from commands2 import Command, CommandScheduler
from RobotContainer import RobotContainer

class MyRobot(TimedRobot):
    # Variable Declaration
    m_robotContainer:RobotContainer = None
    m_autonomousCommand:Command = None

    # Initialization
    def robotInit(self):
        self.m_robotContainer = RobotContainer()

    # Periodic Loop / All Modes
    def robotPeriodic(self):
        CommandScheduler.getInstance().run()

    # Autonomous Mode
    def autonomousInit(self):
        self.m_autonomousCommand = self.m_robotContainer.getAutonomousCommand()
    
    def autonomousPeriodic(self): pass

    def autonomousExit(self):
        if self.m_autonomousCommand != None:
            self.m_autonomousCommand.cancel()

    # Teleop Mode
    def teleopInit(self): pass
    def teleopPeriodic(self): pass
    def teleopExit(self): pass

    # Test Mode
    def testInit(self): pass
    def testPeriodic(self): pass
    def testExit(self): pass

    # Disable Mode
    def disabledInit(self): pass
    def disabledPeriodic(self): pass
    def disabledExit(self): pass

    # Simulation Mode
    def _simulationInit(self): pass
    def _simulationPeriodic(self): pass
    def _simulationExit(self): pass