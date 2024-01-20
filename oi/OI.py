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
        
        Keymap.Intake.INTAKE_IN.whileTrue(commands.IntakeIn(Robot.appendage))
        Keymap.Intake.INTAKE_OUT.whileTrue(commands.IntakeOut(Robot.appendage))
        Keymap.Intake.TRANSFER.whileTrue(commands.TransferNote(Robot.appendage))
        Keymap.Intake.SHOOTER.whileTrue(commands.ShooterActivate(Robot.appendage, 5000))