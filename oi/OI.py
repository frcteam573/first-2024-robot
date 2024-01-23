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
        
        Keymap.Intake.INTAKE_IN.whileTrue(
            InstantCommand(lambda: Robot.appendage.setIntake(-.3))
        ).onFalse(
            InstantCommand(lambda: Robot.appendage.setIntake(0))
        )
        
        Keymap.Intake.INTAKE_OUT.whileTrue(
            InstantCommand(lambda: Robot.appendage.setIntake(.3))
        ).onFalse(
            InstantCommand(lambda: Robot.appendage.setIntake(0))
        )
        Keymap.Intake.TRANSFER.whileTrue(
            InstantCommand(lambda: Robot.appendage.setTransfer(.7))
        ).onFalse(
            InstantCommand(lambda: Robot.appendage.setTransfer(0))
        )
        Keymap.Intake.SHOOTER.whileTrue(
            InstantCommand(lambda: Robot.appendage.setShooter(11000))
        ).onFalse(
            InstantCommand(lambda: Robot.appendage.setShooter(0))
        )
        
        Keymap.Drivetrain.DRIVE_ALIGN_STRAIGHT.onTrue(commands.DrivetrainAlignStraight(Robot.drivetrain))
        
        # Keymap.Drivetrain.DRIVE_PATH.whileTrue(red.path_1)
        # Keymap.Drivetrain.SHOW_DRIVE_PATH.onTrue(red.show_field_command)