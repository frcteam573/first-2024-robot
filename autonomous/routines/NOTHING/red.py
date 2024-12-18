import math

from autonomous.routines.NOTHING.coords.red import (
  initial,
  leave,
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

max_vel: meters_per_second = 1
max_accel: meters_per_second_squared = 3

path_1 = FollowPathCustom(
    subsystem=Robot.drivetrain,
    trajectory=CustomTrajectory(
        start_pose=Pose2d(*leave[0]),
        waypoints=[Translation2d(*x) for x in leave[1]],
        end_pose=Pose2d(*leave[2]),
        max_velocity=max_vel,
        max_accel=max_accel,
        start_velocity=0,
        end_velocity=0,
        rev=False,
    ),
    period=constants.period,
    blue_team=blue_team
)

auto = SequentialCommandGroup(
  WaitCommand(SmartDashboard.getNumber("Auto Delay",10)), #Not the best way but it works for now.
  path_1,
)

routine = AutoRoutine(Pose2d(*initial), auto, blue_team=blue_team)