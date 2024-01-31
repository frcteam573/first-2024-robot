import math

import commands2
import wpilib
from commands2 import (
    InstantCommand,
    ParallelCommandGroup,
    SequentialCommandGroup,
    WaitCommand,
)
from robotpy_toolkit_7407.utils import logger

import commands
import config
from oi.keymap import Controllers, Keymap
from robot_systems import Robot, Sensors

logger.info("Hi, I'm OI!")

class OI:
    @staticmethod
    def init() -> None:
        pass

    @staticmethod
    def map_controls():
        logger.info("Mapping controls...")
        
        Keymap.Intake.INTAKE_IN.whileTrue(
            InstantCommand(lambda: Robot.appendage.setIntakeSpeed(-.3))
        ).onFalse(
            InstantCommand(lambda: Robot.appendage.setIntakeSpeed(0))
        )
        Keymap.Intake.INTAKE_OUT.whileTrue(
            InstantCommand(lambda: Robot.appendage.setIntakeSpeed(.3))
        ).onFalse(
            InstantCommand(lambda: Robot.appendage.setIntakeSpeed(0))
        )
        Keymap.Intake.TRANSFER.whileTrue(
            InstantCommand(lambda: Robot.appendage.setTransferSpeed(1))
        ).onFalse(
            InstantCommand(lambda: Robot.appendage.setTransferSpeed(0))
        )
        commands2.Trigger(lambda: Keymap.Intake.SHOOTER.value < .95).whileTrue(
            InstantCommand(lambda: Robot.appendage.setShooterRPM(11000))
        ).onFalse(
            InstantCommand(lambda: Robot.appendage.setShooterRPM(0))
        )
        
        Keymap.Climber.CLIMBER_UP.whileTrue(
            InstantCommand(lambda: Robot.appendage.setClimberSpeed(-1))
        ).onFalse(
            InstantCommand(lambda: Robot.appendage.setClimberSpeed(0))
        )
        Keymap.Climber.CLIMBER_DOWN.whileTrue(
            InstantCommand(lambda: Robot.appendage.setClimberSpeed(1))
        ).onFalse(
            InstantCommand(lambda: Robot.appendage.setClimberSpeed(0))
        )
        
        Keymap.Drivetrain.DRIVE_STRAIGHTEN_WHEELS.onTrue(commands.DrivetrainAlignStraight(Robot.drivetrain))
        
        Keymap.Drivetrain.DRIVE_ALIGN_NOTE.onTrue(
            InstantCommand(lambda: Sensors.odometry.vision_estimator.limelights[0].change_pipeline(1))
        ).onFalse(
            InstantCommand(lambda: Sensors.odometry.vision_estimator.limelights[0].change_pipeline(0))
        )
        
        Keymap.Drivetrain.DRIVE_ALIGN_SPEAKER.onTrue(
            InstantCommand(lambda: Sensors.odometry.vision_estimator.limelights[0].change_pipeline(2))
        ).onFalse(
            InstantCommand(lambda: Sensors.odometry.vision_estimator.limelights[0].change_pipeline(0))
        )
        