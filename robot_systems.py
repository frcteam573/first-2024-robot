import wpilib
from robotpy_toolkit_7407.subsystem_templates.drivetrain import SwerveGyro
from robotpy_toolkit_7407.sensors.limelight.limelight import LimelightController, Limelight

import subsystems
from sensors import FieldOdometry

class Robot:
    drivetrain = subsystems.Drivetrain()
    climber = subsystems.Climber()
    intake = subsystems.Intake()
    shooter = subsystems.Shooter()
    shoulder = subsystems.Shoulder()
    led = subsystems.LED()
    trap = subsystems.Trap()

class Sensors:
    odometry: FieldOdometry = FieldOdometry(Robot.drivetrain, LimelightController([
        Limelight(0, 0, limelight_name="limelight-target"),
        # Limelight(0, 0, limelight_name="limelight-intake"),
    ]))
    gyro: SwerveGyro