import math

from autonomous.routines.THREE_NOTE.S2S3S.coords.red import (
  initial,
  note_2,
  rotate,
  note_3,
  speaker,
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
    blue_team=blue_team,
)

path_2 = FollowPathCustom(
  subsystem=Robot.drivetrain,
  trajectory=CustomTrajectory(
    start_pose=Pose2d(*note_3[0]),
    waypoints=[Translation2d(*x) for x in note_3[1]],
    end_pose=Pose2d(*note_3[2]),
    max_velocity=max_vel,
    max_accel=max_accel,
    start_velocity=0,
    end_velocity=0,
    rev=False,
  ),
  period=constants.period,
  blue_team=blue_team,
)

path_3 = FollowPathCustom(
  subsystem=Robot.drivetrain,
  trajectory=CustomTrajectory(
    start_pose=Pose2d(*speaker[0]),
    waypoints=[Translation2d(*x) for x in speaker[1]],
    end_pose=Pose2d(*speaker[2]),
    max_velocity=max_vel,
    max_accel=max_accel,
    start_velocity=0,
    end_velocity=0,
    rev=True,
  ),
  period=constants.period,
  blue_team=blue_team,
)

rotate_path = FollowPathCustom(
  subsystem=Robot.drivetrain,
  trajectory=CustomTrajectory(
    start_pose=Pose2d(*rotate[0]),
    waypoints=[Translation2d(*x) for x in rotate[1]],
    end_pose=Pose2d(*rotate[2]),
    max_velocity=max_vel,
    max_accel=max_accel,
    start_velocity=0,
    end_velocity=0,
    rev=True,
  ),
  period=constants.period,
  blue_team=blue_team
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
  commands.SetShoulderAngleSpeakerAuto(Robot.shoulder),
  commands.TransferNote(Robot.intake),
  commands.SetShoulderAngleAuto(Robot.shoulder, config.shoulder_floor_pos),
  rotate_path,
  ParallelDeadlineGroup( # go to note 3 to take in note
    path_2,
    commands.IntakeIn(Robot.intake),
    commands.SetShoulderAngle(Robot.shoulder, config.shoulder_floor_pos),
  ),
  path_3, # drive toward and line up to speaker
  commands.SetShoulderAngleSpeakerAuto(Robot.shoulder),
  commands.TransferNote(Robot.intake),
)

routine = AutoRoutine(Pose2d(*initial), auto, blue_team=blue_team)