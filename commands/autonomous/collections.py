from commands2 import (
    InstantCommand,
    ParallelCommandGroup,
    ParallelDeadlineGroup,
    SequentialCommandGroup,
    WaitCommand,
)
from commands2 import PrintCommand
from wpimath.geometry import Pose2d, Translation2d
from wpilib import SmartDashboard, Field2d

import commands
import config
import constants
from commands.autonomous.custom_pathing import FollowPathCustom, FollowPathCustomAprilTag
from commands.autonomous.trajectory import CustomTrajectory
from autonomous.auto_routine import AutoRoutine
from robot_systems import Robot, Sensors

class AlignAndShoot(SequentialCommandGroup):
  '''
  Speed up shooter

  Wait 0.5 seconds

  Set shoulder to speaker angle

  Transfer note

  Wait 0.1 seconds

  Stop shooter

  Set shoulder to floor position
  '''
  def __init__(self) -> None:
    super().__init__()
    
    self.commands = (
      InstantCommand(lambda: Robot.shooter.setShooterRPM(4000)),
      WaitCommand(0.5),
      commands.SetShoulderAngleSpeakerAuto(Robot.shoulder),
      commands.TransferNoteAuto(Robot.intake),
      WaitCommand(0.1),
      InstantCommand(lambda: Robot.shooter.setShooterRPM(0)),
      commands.SetShoulderAngleAuto(Robot.shoulder, config.shoulder_floor_pos),
    )

    self.addCommands(
      *self.commands
    )