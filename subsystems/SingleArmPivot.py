# Commands imports
from commands2 import Subsystem

# WPILib / NT imports
from wpilib import RobotState, SmartDashboard, RobotBase, RobotController, Mechanism2d, Color8Bit, Color
from wpilib.simulation import SingleJointedArmSim
from wpimath.system.plant import DCMotor
from wpimath.units import *
from ntcore.util import ntproperty # TODO change to Tunables after Ben implements them

# Pheonix imports
from phoenix6.hardware import TalonFX, CANcoder
from phoenix6.signals import InvertedValue, NeutralModeValue, FeedbackSensorSourceValue, GravityTypeValue, SensorDirectionValue, StaticFeedforwardSignValue, GainSchedBehaviorValue
from phoenix6.controls import PositionVoltage, VoltageOut
from phoenix6.sim import ChassisReference
from phoenix6.configs import *
from phoenix6.units import *

# Our own imports
from util.FalconLogger import FalconLogger

class SimConstants:
    simulate_gravity = True
    arm_length = 0.3 # meters - to be estimated based on the actual mechanism, can also be calculated manually if you have the CAD model and know how to calculate it from MOI
    arm_weight = 3.4 # kg - to be estimated based on the actual mechanism, can also be calculated manually if you have the CAD model and know how to calculate it from MOI


class PivotConstants:
    kP:float=0.0   # proportion       The farther away, the harder it pushes
    kI:float=0.0    # integral         The longer it's been off, the harder it pushes
    kD:float=0.0    # differential     The harder it pushes, the less it pushes :ROFL:
    kS:float=0.0    # static           The amount of force required to overcome static friction (friction while not moving)
    kG:float=0.0   # gravity          Constant force, but accounting for gravity - scales by rotation for pivots

    gear_ratio:float=1/2 # rotor/mechanism (example shows one motor for 2 arm rotations, so 1/2)

    tolerance:degrees = 2 # example tolerance for being "at" the setpoint

class TalonFXSingleArmPivot(Subsystem):
    class Positions:
        MIN:degrees = 0
        MAX:degrees = 180
        UP:degrees = 90
        START:degrees = UP

    def __init__(self, motor_id:int, encoder_id:int, encoder_offset:degrees, is_disabled:typing.Callable[[], bool]) -> None:
        # Setup Motor
        self.motor = TalonFX(device_id=motor_id, canbus="rio")

        # Config
        self.motor_config = TalonFXConfiguration()
        self.motor_config = self.motor_config.with_motor_output(
            MotorOutputConfigs()
            .with_neutral_mode(NeutralModeValue.COAST) # may need to be BRAKE depending on how the mechanism behaves when unpowered
            .with_inverted(InvertedValue.CLOCKWISE_POSITIVE) # TODO test if this is the right direction, may need to be COUNTERCLOCKWISE_POSITIVE depending on how the motor is mounted
        ).with_slot0(
            Slot0Configs()
            .with_k_p(PivotConstants.kP)
            .with_k_i(PivotConstants.kI)
            .with_k_d(PivotConstants.kD)
            .with_k_s(PivotConstants.kS)
            .with_k_g(PivotConstants.kG)
            .with_gravity_type(GravityTypeValue.ARM_COSINE)
            .with_gravity_arm_position_offset(0.0) # to be tuned (dif between desired "straight up" and actual up with balance/doesn't fall down either side)
            .with_static_feedforward_sign(StaticFeedforwardSignValue.USE_CLOSED_LOOP_SIGN)
            .with_gain_sched_behavior(GainSchedBehaviorValue.USE_SLOT1)
        ).with_slot1( # example slot 1 configs for gain scheduling - will be used when the error is large to help get to the setpoint faster, then switch to slot 0 for fine tuning when close to the setpoint
            Slot1Configs() # TODO still need to tune it if necesssary
                .with_k_p(0.0)
                .with_k_i(0.0)
                .with_k_d(0.0)
                .with_k_s(0.0)
                .with_k_g(0.0)
                .with_gravity_type(GravityTypeValue.ARM_COSINE)
                .with_gravity_arm_position_offset(0.0)
                .with_static_feedforward_sign(StaticFeedforwardSignValue.USE_CLOSED_LOOP_SIGN)
        ).with_feedback(
            FeedbackConfigs()
                .with_feedback_remote_sensor_id(encoder_id)
                .with_feedback_sensor_source(FeedbackSensorSourceValue.REMOTE_CANCODER) # TODO change REMOTE_CANCODER to type of encoder being used
                .with_rotor_to_sensor_ratio(PivotConstants.gear_ratio) #rotor tooth count / pivot tooth count
                .with_sensor_to_mechanism_ratio(1) # depends on where encoder is mounted in respect to the mechanism (example from REBUILT season with ratio 1:1 is on the intake pivot)
        ).with_closed_loop_general(
            ClosedLoopGeneralConfigs()
                .with_gain_sched_error_threshold(PivotConstants.tolerance / 360) # needed to convert to rotations
        ).with_closed_loop_ramps(
            ClosedLoopRampsConfigs()
                .with_voltage_closed_loop_ramp_period(0.03) # example from REBUILT season intake
        ).with_current_limits(
            CurrentLimitsConfigs()
                .with_stator_current_limit(60) # standard is 120 amps, but lower is better for less power draw
                .with_stator_current_limit_enable(True)
                .with_supply_current_limit(30) # standard is stator limit, but lower is better for efficiency
                .with_supply_current_limit_enable(True)
                .with_supply_current_lower_limit(30)
                .with_supply_current_lower_time(1.0)
        )
        self.motor.configurator.apply(self.motor_config)

        # Setup Encoder
        self.pivot_encoder = CANcoder(device_id=encoder_id, canbus="rio")
        encoder_config = CANcoderConfiguration()\
            .with_magnet_sensor(
                MagnetSensorConfigs()\
                    .with_magnet_offset(encoder_offset) # to be determined experimentally - the angle at which the magnet is detected at 0 degrees of the mechanism
                    .with_sensor_direction(SensorDirectionValue.COUNTER_CLOCKWISE_POSITIVE) # TODO test if this is the right direction, may need to be CLOCKWISE_POSITIVE depending on how the encoder is mounted
            )
        # Apply Config to Encoder
        self.pivot_encoder.configurator.apply(encoder_config)

        ### PID Functionality Setup
        self.pivot_request = PositionVoltage(position=0.0) # arg will be self.getPivotPosition() bc closed loop
        self.disable_pivot = is_disabled

        # Logging
        FalconLogger.addLoggedObject("/SingleArmPivot/PivotEncoder", self.pivot_encoder)
        FalconLogger.addLoggedObject("/SingleArmPivot/PivotMotor", self.motor)

        ## Mech 2d setup for simulation visualization
        self.mech = Mechanism2d( 100, 100, Color8Bit(50, 50, 70) )
        self.mech_root = self.mech.getRoot("Pivot Root", 90, 10 )
        self.mech_rob_base = self.mech_root.appendLigament("Robot base", 50, 180, color=Color8Bit(Color.kGray) )
        self.mech_arm_target = self.mech_rob_base.appendLigament("Arm Target", 40, 0, color=Color8Bit(Color.kYellow), lineWidth=4 )
        self.mech_arm_actual = self.mech_rob_base.appendLigament("Arm Actual", 80, 0, color=Color8Bit(Color.kGreen) )
        if RobotBase.isSimulation(): self.mech_arm_sim = self.mech_rob_base.appendLigament('Arm Sim', 60, 0, color=Color8Bit(Color.kRed) )

        SmartDashboard.putData("/Mechanisms/SingleArmPivot", self.mech)

        ### Simulation Setup
        if RobotBase.isSimulation():

            self.motor_sim = self.motor.sim_state
            self.encoder_sim = self.pivot_encoder.sim_state

            self.motor_sim.set_motor_type(self.motor_sim.MotorType.KRAKEN_X60)
            self.motor_sim.orientation = ChassisReference.COUNTER_CLOCKWISE_POSITIVE # same as encoder direction instantiated before/above
            self.encoder_sim.set_raw_position(degreesToRotations(self.Positions.START)) # starts in start (up) position

            self.arm_sim = SingleJointedArmSim(
                DCMotor.krakenX60(1), # number of motors (example is 1, but if using 2 motors for the pivot, change to 2 and adjust current limits accordingly  
                PivotConstants.gear_ratio, # example gear ratio, change as needed
                SingleJointedArmSim.estimateMOI(SimConstants.arm_length, SimConstants.arm_weight), # len in m, mass in kg - to be estimated based on the actual mechanism, can also be calculated manually if you have the CAD model and know how to calculate MOI from it
                SimConstants.arm_length, # arm length (???)
                degreesToRadians(self.Positions.MIN),
                degreesToRadians(self.Positions.MAX),
                SimConstants.simulate_gravity, # Gravity
                degreesToRadians(self.Positions.START)
            )
            self.arm_sim.setState( degreesToRadians(self.Positions.START), 0.0 ) # start position, velocity
            # could replace self.Positions.START with self.getPivotPosition() if you want to start the sim at the actual position of the pivot, but may not be necessary

    def periodic(self) -> None:
        # Logging: Write Current Measured Subsystem State
        # FalconLogger.logInput("/Intake/Inputs/launchMotor/velocity (rps)", self.motor.get_velocity().value) TODO delete after subsystem completion

        # Run Subsystem (if not disabled)
        if RobotState.isDisabled() or self.disable_pivot:
            self.stop()
        else:
            self.run()

        # Mech 2D Visualization Updates
        self.mech_arm_actual.setAngle( -self.get_pivot_position() ) # forgor why I need -
        self.mech_arm_target.setAngle( -self.get_pivot_setpoint() ) # forgor why I need -

        # Logging: Write Post Operation Information
        FalconLogger.logOutput("/SingleArmPivot/Outputs/PivotSetpoint (deg)", self.get_pivot_setpoint() ) # setpoint
        FalconLogger.logOutput("/SingleArmPivot/Outputs/Error (deg)", self.motor.get_closed_loop_error().value * 360) # error
        FalconLogger.logOutput("/SingleArmPivot/Outputs/ClosedLoopReference (deg)", self.motor.get_closed_loop_reference().value * 360) # pid target
        FalconLogger.logOutput("/SingleArmPivot/Outputs/PivotPosition (deg)", self.get_pivot_position() ) # actual position
        FalconLogger.logOutput("/SingleArmPivot/Outputs/AtSetpoint", self.get_closed_loop_at_setpoint() ) # at setpoint boolean


    def simulationPeriodic(self):
        ## Simulation Physics (honestly dunnno if these have ever worked)
        # set the supply voltage of the TalonFX
        self.motor_sim.set_supply_voltage(RobotController.getBatteryVoltage())
        self.encoder_sim.set_supply_voltage(RobotController.getBatteryVoltage())
        
        # get the motor voltage of the TalonFX
        motor_voltage = self.motor_sim.motor_voltage
        FalconLogger.logOutput('/SingleArmPivot/MotorSimVoltage', motor_voltage)


        # use the motor voltage to calculate new position and velocity
        # using WPILIB's DCMotorSim class for physics simulation
        self.arm_sim.setInputVoltage(motor_voltage)
        self.arm_sim.update(0.020) # assume 20 ms loop time

        # apply the new rotor position and velocity to the Talon FX;
        # note that this is rotor position/veloicty (before gear ratio), but
        # DCMotorSim returns mechanism position/velocity (after gear ratio), so we need to convert
        self.motor_sim.set_raw_rotor_position(
            PivotConstants.gear_ratio
            * radiansToRotations(self.arm_sim.getAngle())
        )
        self.motor_sim.set_rotor_velocity(
            PivotConstants.gear_ratio
            * radiansToRotations(self.arm_sim.getVelocity())
        )
        self.encoder_sim.set_raw_position(
            radiansToRotations(self.arm_sim.getAngle())
        )
        self.encoder_sim.set_velocity(
            radiansToRotations(self.arm_sim.getVelocity())
        )
    
    def run(self):
        ## Pivot
        # control position
        if not self.disable_pivot:
            if abs(self.pivot_request.position * 360 - self.get_pivot_position()) > PivotConstants.tolerance:
                self.motor.set_control(VoltageOut(0.0)) # if within tol, do nothing
            else:
                self.motor.set_control(self.pivot_request)
        else:
            self.motor.set_control(VoltageOut(0.0)) # if disabled, always do nothing
    
    def toggle_disabled(self) -> None:
        self.disable_pivot = not self.disable_pivot

    def stop(self) -> None:
        pass
        #tbd on implementation

    def set_pivot_setpoint(self, setpoint:degrees) -> None:
        self.pivot_request.position = min(max(setpoint, self.Positions.MIN), self.Positions.MAX) / 360 # deg to rot with normalization

    def get_pivot_setpoint(self) -> degrees:
        return self.pivot_request.position * 360
    
    def get_pivot_position(self) -> degrees:
        return self.pivot_encoder.get_absolute_position().value * 360 # rot to deg
    
    def get_closed_loop_at_setpoint(self, override_tol:degrees=None) -> bool:
        """
        Gets the closed loop error from the motor and checks if it's within the tolerance to determine if at setpoint - may be slower than get_at_setpoint which calculates error manually, but not sure yet
        """
        return abs(self.motor.get_closed_loop_error().value * 360) < (PivotConstants.tolerance if override_tol == None else override_tol)
    
    def get_at_setpoint(self, override_tol:degrees=None) -> bool:
        """
        Another way to determine if pivot at setpoints but through manual error calculation
        This may be faster (update earlier) than the closed loop error? idk
        """
        return abs(self.getPivotPosition() - self.getPivotSetpoint()) < (PivotConstants.tolerance if override_tol == None else override_tol)