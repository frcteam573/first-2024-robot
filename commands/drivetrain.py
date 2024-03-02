import logging
import math

import commands2
from commands2 import SequentialCommandGroup
from robotpy_toolkit_7407.command import SubsystemCommand
from wpimath.controller import PIDController
from wpimath.geometry import Pose2d, Rotation2d
from wpimath.filter import SlewRateLimiter
import commands
import wpilib
import config
import constants
from robot_systems import Sensors
from sensors import FieldOdometry
from subsytems import Drivetrain


def curve_abs(x):
    curve = wpilib.SmartDashboard.getNumber('curve', 2)
    return x**curve


def curve(x):
    if x < 0:
        return -curve_abs(-x)
    return curve_abs(x)


class DriveSwerveCustom(SubsystemCommand[Drivetrain]):
    driver_centric = True
    driver_centric_reversed = False
    period = constants.period
    angular_pid: PIDController = PIDController(1, 0.5, 0.05)
    target_pid: PIDController = PIDController(.02, 0, 0)
    speaker_pid: PIDController = PIDController(.03, .001, 0)
    target_angle = None

    def initialize(self) -> None:
        self.angular_pid.setSetpoint(0)
        self.target_pid.setSetpoint(0)
        self.speaker_pid.setSetpoint(0)
        self.target_angle = Sensors.gyro.get_robot_heading() % (math.pi * 2)
        self.target_angle = math.atan2(
            math.sin(self.target_angle), math.cos(self.target_angle)
        )
        self.base_accel = constants.drivetrain_max_accel_tele
        self.accel = wpilib.SmartDashboard.getNumber('tele_accel', self.base_accel)
        self.ramp_limit_x = SlewRateLimiter(self.accel, -self.accel, 0.0)
        self.ramp_limit_y = SlewRateLimiter(self.accel, -self.accel, 0.0)
    def execute(self) -> None:
        
        #might be better to add acceleration after scaling if its non-linear
        
        current_angle = Sensors.odometry.getPose().rotation()
        relative = Pose2d(0, 0, self.target_angle).relativeTo(
            Pose2d(0, 0, current_angle)
        )
        angular_vel = self.angular_pid.calculate(abs(relative.rotation().radians())) * (
            -1 if relative.rotation().radians() > 0 else 1
        )
        
        dx, dy, d_theta = (
            self.subsystem.axis_dx.value * (-1 if config.drivetrain_reversed else 1),
            self.subsystem.axis_dy.value * (-1 if config.drivetrain_reversed else 1),
            -self.subsystem.axis_rotation.value,
        )

# ---------------- This is the speaker tag auto align and gyro stablization block. Can be commented out for basic swerve joystick control
        tag_aligned = False
        note_align = self.subsystem.note_align_button.getAsBoolean()
        speaker_align = self.subsystem.speaker_align_button.getAsBoolean()
        if note_align or speaker_align:
            # tx = Rotation2d.fromDegrees(Sensors.odometry.limelight_intake.get_tx())
            # current_angle -= tx
            tx = None
            if note_align:

                mag = ((dx**2 + dy**2)**0.5)*0.3

                tx = Sensors.odometry.vision_estimator.limelights[1].get_tx()
                dx = mag * math.sin(Sensors.gyro.get_robot_heading()) * (1 if config.drivetrain_reversed else -1)
                dy = mag * math.cos(Sensors.gyro.get_robot_heading()) * (1 if config.drivetrain_reversed else -1)
                if tx:
                    d_theta = self.target_pid.calculate(tx)
            elif speaker_align:
                tx = Sensors.odometry.vision_estimator.limelights[0].get_tx()
                if not tx:
                    tx = Sensors.odometry.getAngleToPose(
                        (constants.ApriltagPositionDictBlue[7] if config.blue_team else constants.ApriltagPositionDictRed[4]).toPose2d()
                        )
                d_theta = self.speaker_pid.calculate(tx)
                if abs(d_theta) > 0.5:
                    d_theta = d_theta / abs(d_theta) * 0.5
            if tx:
                tag_aligned = abs(tx) < config.vision_threshold
            self.target_angle = current_angle
        # elif abs(d_theta) < 0.11: # This is for gyro stablization
        #     d_theta = angular_vel
        # else:
        #     self.target_angle = current_angle
        wpilib.SmartDashboard.putBoolean("Tag aligned", tag_aligned)
# ----------------------------------------------------------------------------------------
        #print("SwerveDriveCustom")
        #print("dx", dx)
        dx = curve(dx)
        dy = curve(dy)
        d_theta = curve(d_theta)

        dx *= self.subsystem.max_vel
        dy *= -self.subsystem.max_vel
        d_theta *= self.subsystem.max_angular_vel

        # if dx == 0 and dy == 0 and d_theta == 0:
        #     self.subsystem.n_front_left.zero()
        #     self.subsystem.n_front_right.zero()
        #     self.subsystem.n_back_left.zero()
        #     self.subsystem.n_back_right.zero()
        #
        #     self.subsystem.n_front_left.set_motor_angle(0)
        #     self.subsystem.n_front_right.set_motor_angle(0)
        #     self.subsystem.n_back_left.set_motor_angle(0)
        #     self.subsystem.n_back_right.set_motor_angle(0)


        if constants.drivetrain_accel:
            dx_scale = dx
            dy_scale = dy

            dx = self.ramp_limit_x.calculate(dx)
            dy = self.ramp_limit_y.calculate(dy)
        
            ## deceleration
            if abs(dx) > abs(dx_scale):
                dx = dx_scale

            
            if abs(dy) > abs(dy_scale):
                dy = dy_scale



        if config.driver_centric:
            self.subsystem.set_driver_centric((-dy, dx), d_theta)
        elif self.driver_centric_reversed:
            self.subsystem.set_driver_centric((dy, -dx), -d_theta)
        else:
            self.subsystem.set_robot_centric((dy, -dx), d_theta)

    def end(self, interrupted: bool) -> None:
        self.subsystem.n_front_left.set_motor_velocity(0)
        self.subsystem.n_front_right.set_motor_velocity(0)
        self.subsystem.n_back_left.set_motor_velocity(0)
        self.subsystem.n_back_right.set_motor_velocity(0)
        self.ramp_limit_x.reset(0)
        self.ramp_limit_y.reset(0)

    def isFinished(self) -> bool:
        return False

    def runsWhenDisabled(self) -> bool:
        return False


class DrivetrainZero(SubsystemCommand[Drivetrain]):
    def __init__(self, subsystem: Drivetrain):
        super().__init__(subsystem)
        self.subsystem = subsystem

    def initialize(self) -> None:
        #print("ZEROING DRIVETRAIN")
        self.subsystem.n_front_left.zero()
        self.subsystem.n_front_right.zero()
        self.subsystem.n_back_left.zero()
        self.subsystem.n_back_right.zero()

    def execute(self) -> None:
        ...

    def isFinished(self) -> bool:
        ...
        return True

    def end(self, interrupted: bool) -> None:
        logging.info("Successfully re-zeroed swerve pods.")
        ...


class DriveSwerveSlowed(SubsystemCommand[Drivetrain]):
    driver_centric = True
    driver_centric_reversed = False
    angular_pid = None
    target_angle = Rotation2d(0)

    def initialize(self) -> None:
        #print("STARTED DRIVE SWERVE SLOW")
        self.angular_pid: PIDController = PIDController(2, 0, 0.05)
        self.angular_pid.setSetpoint(0)

        gyro_angle = self.subsystem.gyro.get_robot_heading() % (math.pi * 2)
        gyro_angle = math.degrees(
            math.atan2(math.sin(gyro_angle), math.cos(gyro_angle))
        )

        if -90 < gyro_angle < 90:
            self.target_angle = Rotation2d(0)
        else:
            self.target_angle = Rotation2d(math.pi)

    def execute(self) -> None:
        current_angle = Sensors.odometry.getPose().rotation()
        relative = Pose2d(0, 0, self.target_angle).relativeTo(
            Pose2d(0, 0, current_angle)
        )

        angular_vel = self.angular_pid.calculate(abs(relative.rotation().radians())) * (
            -1 if relative.rotation().radians() > 0 else 1
        )

        dx, dy, d_theta = (
            self.subsystem.axis_dx.value * (-1 if config.drivetrain_reversed else 1),
            self.subsystem.axis_dy.value * (-1 if config.drivetrain_reversed else 1),
            angular_vel,
        )

        dx = curve(dx)
        dy = curve(dy)

        dx *= config.drivetrain_scoring_velocity * 2.5
        dy *= -config.drivetrain_scoring_velocity * 2.5
        d_theta = min(config.drivetrain_scoring_angular_velocity, d_theta)

        controller_d_theta = -self.subsystem.axis_rotation.value

        if abs(controller_d_theta) > 0.15:
            d_theta = (
                curve(controller_d_theta) * config.drivetrain_scoring_angular_velocity
            )

        self.subsystem.set_driver_centric((-dy, dx), d_theta)

    def end(self, interrupted: bool) -> None:
        self.subsystem.n_front_left.set_motor_velocity(0)
        self.subsystem.n_front_right.set_motor_velocity(0)
        self.subsystem.n_back_left.set_motor_velocity(0)
        self.subsystem.n_back_right.set_motor_velocity(0)

    def isFinished(self) -> bool:
        return False

    def runsWhenDisabled(self) -> bool:
        return False


class DrivetrainScoreSlow(SubsystemCommand[Drivetrain]):
    def __init__(self, subsystem: Drivetrain):
        super().__init__(subsystem)
        self.subsystem = subsystem

    def initialize(self) -> None:
        commands2.CommandScheduler.getInstance().schedule(
            commands.DriveSwerveSlowed(self.subsystem)
        )

    def isFinished(self) -> bool:
        return True

    def end(self, interrupted: bool) -> None:
        ...


class DrivetrainScoreFront(SubsystemCommand[Drivetrain]):
    def __init__(self, subsystem: Drivetrain, odometry: FieldOdometry):
        super().__init__(subsystem)
        self.subsystem = subsystem
        self.odometry = odometry

    def initialize(self) -> None:
        # config.driver_centric = False
        config.drivetrain_reversed = True

        self.odometry.vision_on = False
        current_theta = self.odometry.getPose().rotation().degrees()

        if -90 < current_theta < 90:
            desired_theta = 0
        else:
            desired_theta = math.radians(180)

        self.subsystem.max_vel = config.drivetrain_scoring_velocity
        self.subsystem.max_angular_vel = config.drivetrain_scoring_angular_velocity

        commands2.CommandScheduler.getInstance().schedule(
            SequentialCommandGroup(
                # command.autonomous.custom_pathing.RotateInPlace(
                #     self.subsystem,
                #     threshold=math.radians(6),
                #     theta_f=desired_theta,
                #     max_angular_vel=config.drivetrain_scoring_angular_velocity,
                # ),
                commands.DriveSwerveCustom(self.subsystem),
            )
        )

    def isFinished(self) -> bool:
        return True

    def end(self, interrupted: bool) -> None:
        ...


class DrivetrainRegular(SubsystemCommand[Drivetrain]):
    def __init__(self, subsystem: Drivetrain, odometry: FieldOdometry):
        super().__init__(subsystem)
        self.subsystem = subsystem
        self.odometry = odometry

    def initialize(self) -> None:
        config.drivetrain_reversed = False

        commands2.CommandScheduler.getInstance().schedule(
            commands.DriveSwerveCustom(self.subsystem)
        )

    def isFinished(self) -> bool:
        return True

    def end(self, interrupted: bool) -> None:
        ...
        

class DrivetrainAlignStraight(SubsystemCommand[Drivetrain]):
    def __init__(self, subsystem: Drivetrain):
        super().__init__(subsystem)
        self.subsystem = subsystem

    def initialize(self) -> None:
        self.subsystem.n_front_left.set_motor_angle(0)
        self.subsystem.n_front_right.set_motor_angle(0)
        self.subsystem.n_back_left.set_motor_angle(0)
        self.subsystem.n_back_right.set_motor_angle(0)

    def isFinished(self) -> bool:
        return True

    def end(self, interrupted: bool) -> None:
        ...
