import math

from autonomous.routines.TWO_DISC.coords.red import (
    blue_team,
    go_back_1m,
    go_forward_1m,
    initial,
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
import commands.autonomous.collections as collections
from commands.autonomous.custom_pathing import FollowPathCustom
from commands.autonomous.trajectory import CustomTrajectory
from autonomous.auto_routine import AutoRoutine
from robot_systems import Robot, Sensors
from units.SI import meters_per_second, meters_per_second_squared

max_vel: meters_per_second = 4
max_accel: meters_per_second_squared = 3

path_1 = FollowPathCustom(
    subsystem=Robot.drivetrain,
    trajectory=CustomTrajectory(
        start_pose=Pose2d(*go_back_1m[0]),
        waypoints=[Translation2d(*x) for x in go_back_1m[1]],
        end_pose=Pose2d(*go_back_1m[2]),
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
        start_pose=Pose2d(*go_forward_1m[0]),
        waypoints=[Translation2d(*x) for x in go_forward_1m[1]],
        end_pose=Pose2d(*go_forward_1m[2]),
        max_velocity=max_vel,
        max_accel=max_accel,
        start_velocity=0,
        end_velocity=0,
    ),
    period=constants.period,
)

auto = SequentialCommandGroup(
    path_1,
    InstantCommand(lambda: print("intake in")),
    WaitCommand(1),
    InstantCommand(lambda: print("intake stop")),
    path_2,
)

routine = AutoRoutine(Pose2d(*initial), auto, blue_team=blue_team)

def show_field():
    field = Field2d()
    field.getObject("traj").setTrajectory(path_1.trajectory)
    SmartDashboard.putData("Field", field)
    print("called show_field")

show_field_command = InstantCommand(show_field)