import math

from autonomous.routines.THREE_NOTE.S1S2S.coords.blue import (
  initial,
  note_2,
  note_2_to_speaker,
  note_1,
  note_1_to_speaker,
  blue_team
)

from commands2 import (
    InstantCommand,
    ParallelCommandGroup,
    ParallelDeadlineGroup,
    SequentialCommandGroup,
    WaitCommand,
)
from wpimath.geometry import Pose2d, Translation2d
from wpilib import SmartDashboard, Field2d

import commands
import config
import constants
from commands.autonomous.custom_pathing import FollowPathCustom, FollowPathCustomAprilTag
from commands.autonomous.trajectory import CustomTrajectory
from autonomous.auto_routine import AutoRoutine
from robot_systems import Robot, Sensors
from units.SI import meters_per_second, meters_per_second_squared

max_vel: meters_per_second = 1
max_accel: meters_per_second_squared = 3

path_1 = FollowPathCustom(
    subsystem=Robot.drivetrain,
    trajectory=CustomTrajectory(
        start_pose=Pose2d(*note_2[0]),
        waypoints=[Translation2d(*x) for x in note_2[1]],
        end_pose=Pose2d(*note_2[2]),
        max_velocity=max_vel,
        max_accel=max_accel,
        start_velocity=0,
        end_velocity=0,
        rev=False,
    ),
    period=constants.period,
)

path_2 = FollowPathCustom(
    subsystem=Robot.drivetrain,
    trajectory=CustomTrajectory(
        start_pose=Pose2d(*note_2_to_speaker[0]),
        waypoints=[Translation2d(*x) for x in note_2_to_speaker[1]],
        end_pose=Pose2d(*note_2_to_speaker[2]),
        max_velocity=max_vel,
        max_accel=max_accel,
        start_velocity=0,
        end_velocity=0,
        rev=True,
    ),
    period=constants.period,
)

path_3 = FollowPathCustom(
    subsystem=Robot.drivetrain,
    trajectory=CustomTrajectory(
        start_pose=Pose2d(*note_1[0]),
        waypoints=[Translation2d(*x) for x in note_1[1]],
        end_pose=Pose2d(*note_1[2]),
        max_velocity=max_vel,
        max_accel=max_accel,
        start_velocity=0,
        end_velocity=0,
        rev=True,
    ),
    period=constants.period,
)

path_4 = FollowPathCustom(
    subsystem=Robot.drivetrain,
    trajectory=CustomTrajectory(
        start_pose=Pose2d(*note_1_to_speaker[0]),
        waypoints=[Translation2d(*x) for x in note_1_to_speaker[1]],
        end_pose=Pose2d(*note_1_to_speaker[2]),
        max_velocity=max_vel,
        max_accel=max_accel,
        start_velocity=0,
        end_velocity=0,
        rev=True,
    ),
    period=constants.period,
)

auto = SequentialCommandGroup(
  InstantCommand(lambda: Robot.shooter.setShooterRPM(4000)),
  commands.SetShoulderAngleSpeakerAuto(Robot.shoulder),
  commands.TransferNote(Robot.intake),
  commands.SetShoulderAngleAuto(Robot.shoulder, config.shoulder_floor_pos),
  ParallelDeadlineGroup( # go to note 2 to take in note
    path_1,
    commands.IntakeIn(Robot.intake),
    commands.SetShoulderAngle(Robot.shoulder, config.shoulder_floor_pos),
  ),
  path_2,
  commands.SetShoulderAngleSpeakerAuto(Robot.shoulder),
  commands.TransferNote(Robot.intake),
  commands.SetShoulderAngleAuto(Robot.shoulder, config.shoulder_floor_pos),
  ParallelDeadlineGroup( # go to note 1 to take in note
    path_3,
    commands.IntakeIn(Robot.intake),
    commands.SetShoulderAngle(Robot.shoulder, config.shoulder_floor_pos),
  ),
  path_4, # drive toward and line up to speaker
  commands.SetShoulderAngleSpeakerAuto(Robot.shoulder),
  commands.TransferNote(Robot.intake),
)

routine = AutoRoutine(Pose2d(*initial), auto, blue_team=blue_team)