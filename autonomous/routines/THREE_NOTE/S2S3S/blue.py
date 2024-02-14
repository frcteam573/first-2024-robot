import math

from autonomous.routines.THREE_NOTE.S2S3S.coords.blue import (
  initial,
  note_2,
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
        rev=True,
    ),
    period=constants.period,
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
)

path_3 = FollowPathCustomAprilTag(
  subsystem=Robot.drivetrain,
  trajectory=CustomTrajectory(
    start_pose=Pose2d(*speaker[0]),
    waypoints=[Translation2d(*x) for x in speaker[1]],
    end_pose=Pose2d(*speaker[2]),
    max_velocity=max_vel,
    max_accel=max_accel,
    start_velocity=0,
    end_velocity=0,
    rev=False,
  ),
  limelight=Sensors.odometry.vision_estimator.limelights[0],
  period=constants.period,
)

auto = SequentialCommandGroup(
  # shoot note
  path_1,
  # shoot note
  path_2,
  InstantCommand(lambda: Sensors.odometry.vision_estimator.limelights[0].change_pipeline(2)),
  path_3,
  InstantCommand(lambda: Sensors.odometry.vision_estimator.limelights[0].change_pipeline(0)),
  # shoot note
)

routine = AutoRoutine(Pose2d(*initial), auto, blue_team=blue_team)