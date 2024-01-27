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

from paths import red

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
        
        # Keymap.Intake.INTAKE_IN.whileTrue(
        #     InstantCommand(lambda: Robot.appendage.setIntake(-.3))
        # ).onFalse(
        #     InstantCommand(lambda: Robot.appendage.setIntake(0))
        # )
        # Keymap.Intake.INTAKE_OUT.whileTrue(
        #     InstantCommand(lambda: Robot.appendage.setIntake(.3))
        # ).onFalse(
        #     InstantCommand(lambda: Robot.appendage.setIntake(0))
        # )
        # Keymap.Intake.TRANSFER.whileTrue(
        #     InstantCommand(lambda: Robot.appendage.setTransfer(1))
        # ).onFalse(
        #     InstantCommand(lambda: Robot.appendage.setTransfer(0))
        # )
        # Keymap.Intake.SHOOTER.whileTrue(
        #     InstantCommand(lambda: Robot.appendage.setShooter(11000))
        # ).onFalse(
        #     InstantCommand(lambda: Robot.appendage.setShooter(0))
        # )
        
        Keymap.Drivetrain.DRIVE_ALIGN_STRAIGHT.onTrue(commands.DrivetrainAlignStraight(Robot.drivetrain))
        
        Keymap.Drivetrain.DRIVE_BACK_PATH.whileTrue(red.path_1)
        Keymap.Drivetrain.DRIVE_FORWARD_PATH.whileTrue(red.path_2)
        Keymap.Drivetrain.SHOW_DRIVE_PATH.onTrue(red.show_field_command)
        
        Keymap.Drivetrain.DRIVE_ALIGN_NOTE.onTrue(
            InstantCommand(lambda: Sensors.odometry.vision_estimator.limelights[0].change_pipeline(1))
        ).onFalse(
            InstantCommand(lambda: Sensors.odometry.vision_estimator.limelights[0].change_pipeline(0))
        )
        
        commands2.Trigger(lambda: Keymap.Drivetrain.DRIVE_ALIGN_TARGET.value > .05).onTrue(
            InstantCommand(lambda: Sensors.odometry.vision_estimator.limelights[0].change_pipeline(2))
        ).onFalse(
            InstantCommand(lambda: Sensors.odometry.vision_estimator.limelights[0].change_pipeline(0))
        )