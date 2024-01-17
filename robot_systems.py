import wpilib
from robotpy_toolkit_7407.subsystem_templates.drivetrain import SwerveGyro

import subsytems
from sensors import FieldOdometry

class Robot:
    # arm = subsytems.Arm()
    drivetrain = subsytems.Drivetrain()
    appendage = subsytems.Appendage()
    # climber = subsytems.Climber()
    # intake = subsytems.Intake()
    # grabber = subsytems.Grabber()

class Sensors:
    odometry: FieldOdometry = FieldOdometry(Robot.drivetrain, None)
    gyro: SwerveGyro