from wpilib import TimedRobot, XboxController

from ntcore.util import ntproperty 

from phoenix6.hardware import TalonFX # Motor controller class for Falcons & Krakens

class MyRobot(TimedRobot):
    '''
    A simple project to give manual control of 2 motors with Networktables controllable speeds
    to use this file while in a robot project add the argument `--main runmotor.py` after robotpy (e.g. `robotpy --main runmotor.py deploy`)
    '''

    kraken1_speed_mult = ntproperty("/motor1 speed mult", 1.0)
    kraken2_speed_mult = ntproperty("/motor2 speed mult", 1.0)
    # adds "motor1 speed mult" as an editable property on the networktables
    # this allows for the value to be adjusted without redeploying through programs like Glass or Shuffleboard

    def __init__(self):
        super().__init__()
        self.kraken1 = TalonFX(device_id=0)
        self.kraken2 = TalonFX(device_id=1)
        
        self.controller = XboxController(0)
        
    def teleopPeriodic(self):
        '''
        Runs every frame while the robot is enabled and in Teleop
        '''
        self.kraken1.set(
            self.controller.getRightTriggerAxis() * min(max(self.kraken1_speed_mult, -1), 1) # sets motor speed to the trigger axis times the multiplayer, restricted to [-1,1]
        )
        self.kraken2.set(
            self.controller.getLeftTriggerAxis() * min(max(self.kraken2_speed_mult, -1), 1) # sets motor speed to the trigger axis times the multiplayer, restricted to [-1,1]
        )