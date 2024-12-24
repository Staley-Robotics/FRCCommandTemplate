# Python Imports
from pathlib import Path

# FRC Imports
from wpilib import DriverStation, DataLogManager, RobotBase, TimedRobot
from commands2 import Command, CommandScheduler

# Local Imports
from RobotContainer import RobotContainer
from util import FalconLogger

class MyRobot(TimedRobot):
    # Variable Declaration
    __robotContainer:RobotContainer = None
    __autoCmd:Command = None
    __logger:FalconLogger = None

    # Initialization
    def robotInit(self):
        # Disable Joystick Notifications
        DriverStation.silenceJoystickConnectionWarning(True)

        # Start Logging using the built in DataLogManager
        logDir = '/U/logs' if RobotBase.isReal() else '.logs'
        DataLogManager.start( dir=(logDir if Path(logDir).is_dir() else ''), period=1.0 )
        DriverStation.startDataLog( DataLogManager.getLog() )
        
        # Built The Robot
        self.__robotContainer = RobotContainer()
        self.__logger = FalconLogger(False)

    # Periodic Loop / All Modes
    def robotPeriodic(self):
        # Mark the Current Timestamp for Logging
        self.__logger.setTime()

        # Run the CommandScheduler Loop
        CommandScheduler.getInstance().run()

        # Write the Log Results
        try:
            self.__logger.writeLog()
        except:
            print("WARNING! FalconLogger Cannot Write to Log!")

    # Autonomous Mode
    def autonomousInit(self):
        # Start the Autonomous Package
        try:
            self.__autoCmd = self.__robotContainer.getAutonomousCommand()
            self.__autoCmd.schedule()
        except:
            print("WARNING! getAutonomousCommand failed!")
    
    def autonomousPeriodic(self): pass

    def autonomousExit(self):
        # End the Autonomous Package
        try:
            self.__autoCmd.cancel()
        except:
            pass

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