import math

from autonomous.routines.TWO_NOTE.SC5S.coords.red import (
  initial,
  note_c5,
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
from wpilib.shuffleboard import Shuffleboard

import commands
import config
import constants
import commands.autonomous.collections as collections
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
    start_pose=Pose2d(*note_c5[0]),
    waypoints=[Translation2d(*x) for x in note_c5[1]],
    end_pose=Pose2d(*note_c5[2]),
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
)

auto = SequentialCommandGroup(
  collections.AlignAndShoot(),
  ParallelDeadlineGroup( # go to note 2 to take in note
    path_1,
    commands.IntakeIn(Robot.intake),
    commands.SetShoulderAngle(Robot.shoulder, config.shoulder_floor_pos),
  ),
  ParallelCommandGroup( # go to speaker while shooting
    path_2,
    commands.IntakeIn(Robot.intake),
    SequentialCommandGroup(
      WaitCommand(1.5),
      commands.SetShoulderAngle(Robot.shoulder, config.shoulder_front_speaker),
    ),
  ),
  collections.AlignAndShoot(),
)

routine = AutoRoutine(Pose2d(*initial), auto, blue_team=blue_team)