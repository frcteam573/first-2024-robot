import wpilib
from robotpy_toolkit_7407.subsystem_templates.drivetrain import SwerveGyro
from robotpy_toolkit_7407.sensors.limelight.limelight import LimelightController, Limelight

import subsytems
from sensors import FieldOdometry

class Robot:
    drivetrain = subsytems.Drivetrain()
    climber = subsytems.Climber()
    intake = subsytems.Intake()
    shooter = subsytems.Shooter()
    shoulder = subsytems.Shoulder()
    led = subsytems.LED()

class Sensors:
    odometry: FieldOdometry = FieldOdometry(Robot.drivetrain, LimelightController([
        Limelight(0, 0, limelight_name="limelight-target"),
        Limelight(0, 0, limelight_name="limelight-intake"),
    ]))
    gyro: SwerveGyro