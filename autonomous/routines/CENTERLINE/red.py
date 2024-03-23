import math

from autonomous.routines.CENTERLINE.coords.red import (
  initial,
  path_1,
  path_2,
  path_3,
  path_4,
  path_5,
  path_6,
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
from wpilib.shuffleboard import Shuffleboard

import commands
import config
import constants
from commands.autonomous.custom_pathing import FollowPathCustom, FollowPathCustomAprilTag
from commands.autonomous.trajectory import CustomTrajectory
from autonomous.auto_routine import AutoRoutine
from robot_systems import Robot, Sensors
from units.SI import meters_per_second, meters_per_second_squared

max_vel: meters_per_second = 3
max_accel: meters_per_second_squared = 5

path_1 = FollowPathCustom(
    subsystem=Robot.drivetrain,
    trajectory=CustomTrajectory(
        start_pose=Pose2d(*path_1[0]),
        waypoints=[Translation2d(*x) for x in path_1[1]],
        end_pose=Pose2d(*path_1[2]),
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
        start_pose=Pose2d(*path_2[0]),
        waypoints=[Translation2d(*x) for x in path_2[1]],
        end_pose=Pose2d(*path_2[2]),
        max_velocity=max_vel,
        max_accel=max_accel,
        start_velocity=0,
        end_velocity=0,
        rev=True,
    ),
    period=constants.period,
    blue_team=blue_team,
)

path_3 = FollowPathCustom(
    subsystem=Robot.drivetrain,
    trajectory=CustomTrajectory(
        start_pose=Pose2d(*path_3[0]),
        waypoints=[Translation2d(*x) for x in path_3[1]],
        end_pose=Pose2d(*path_3[2]),
        max_velocity=max_vel,
        max_accel=max_accel,
        start_velocity=0,
        end_velocity=0,
        rev=False,
    ),
    period=constants.period,
    blue_team=blue_team,
)

path_4 = FollowPathCustom(
    subsystem=Robot.drivetrain,
    trajectory=CustomTrajectory(
        start_pose=Pose2d(*path_4[0]),
        waypoints=[Translation2d(*x) for x in path_4[1]],
        end_pose=Pose2d(*path_4[2]),
        max_velocity=max_vel,
        max_accel=max_accel,
        start_velocity=0,
        end_velocity=0,
        rev=True,
    ),
    period=constants.period,
    blue_team=blue_team,
)

path_5 = FollowPathCustom(
    subsystem=Robot.drivetrain,
    trajectory=CustomTrajectory(
        start_pose=Pose2d(*path_5[0]),
        waypoints=[Translation2d(*x) for x in path_5[1]],
        end_pose=Pose2d(*path_5[2]),
        max_velocity=max_vel,
        max_accel=max_accel,
        start_velocity=0,
        end_velocity=0,
        rev=False,
    ),
    period=constants.period,
    blue_team=blue_team,
)

path_6 = FollowPathCustom(
    subsystem=Robot.drivetrain,
    trajectory=CustomTrajectory(
        start_pose=Pose2d(*path_6[0]),
        waypoints=[Translation2d(*x) for x in path_6[1]],
        end_pose=Pose2d(*path_6[2]),
        max_velocity=max_vel,
        max_accel=max_accel,
        start_velocity=0,
        end_velocity=0,
        rev=True,
    ),
    period=constants.period,
    blue_team=blue_team,
)

auto = SequentialCommandGroup(
    InstantCommand(lambda: Robot.shooter.setShooterRPM(4000)),
  ParallelDeadlineGroup( # go to note 2 to take in note
    path_1,
    commands.IntakeIn(Robot.intake),
    commands.SetShoulderAngle(Robot.shoulder, config.shoulder_floor_pos_auto),
  ),
  ParallelDeadlineGroup( # go to note 2 to take in note
    path_2,
    commands.IntakeIn(Robot.intake),
    commands.SetShoulderAngle(Robot.shoulder, config.shoulder_mid_pos),
  ),
  commands.SetShoulderAngle(Robot.shoulder, config.shoulder_amp_pos),
  commands.TransferNoteAuto(Robot.intake),
  commands.SetShoulderAngleAuto(Robot.shoulder, config.shoulder_floor_pos),
  ParallelDeadlineGroup( # go to note 2 to take in note
    path_3,
    commands.IntakeIn(Robot.intake),
    commands.SetShoulderAngle(Robot.shoulder, config.shoulder_floor_pos_auto),
  ),
  ParallelDeadlineGroup( # go to note 2 to take in note
    path_4,
    commands.IntakeIn(Robot.intake),
    commands.SetShoulderAngle(Robot.shoulder, config.shoulder_mid_pos),
  ),
  commands.SetShoulderAngle(Robot.shoulder, config.shoulder_amp_pos),
  commands.TransferNoteAuto(Robot.intake),
  commands.SetShoulderAngleAuto(Robot.shoulder, config.shoulder_floor_pos),
    ParallelDeadlineGroup( # go to note 2 to take in note
    path_5,
    commands.IntakeIn(Robot.intake),
    commands.SetShoulderAngle(Robot.shoulder, config.shoulder_floor_pos_auto),
  ),
  ParallelDeadlineGroup( # go to note 2 to take in note
    path_6,
    commands.IntakeIn(Robot.intake),
    commands.SetShoulderAngle(Robot.shoulder, config.shoulder_mid_pos),
  ),
  commands.SetShoulderAngle(Robot.shoulder, config.shoulder_amp_pos),
  commands.TransferNoteAuto(Robot.intake),
  InstantCommand(lambda: Robot.shooter.setShooterRPM(0)),
)


routine = AutoRoutine(Pose2d(*initial), auto, blue_team=blue_team)