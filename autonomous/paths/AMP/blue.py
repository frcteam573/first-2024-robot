import math

from autonomous.paths.AMP.coords.blue import (
    blue_team,
    go_to_amp,
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
        start_pose=Pose2d(*go_to_amp[0]),
        waypoints=[Translation2d(*x) for x in go_to_amp[1]],
        end_pose=Pose2d(*go_to_amp[2]),
        max_velocity=max_vel,
        max_accel=max_accel,
        start_velocity=0,
        end_velocity=0,
        rev=True,
        use_robot=True,
    ),
    period=constants.period,
)

auto = SequentialCommandGroup(
    path_1
)

routine = AutoRoutine(Pose2d(*initial), auto, blue_team=blue_team)