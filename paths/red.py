import math

from paths.coords.move_back_2m import (
    blue_team,
    go_back_2m,
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

import commands
import config
import constants
from commands.autonomous.custom_pathing import FollowPathCustom
from commands.autonomous.trajectory import CustomTrajectory
from robot_systems import Robot, Sensors
from units.SI import meters_per_second, meters_per_second_squared

max_vel: meters_per_second = 4.5
max_accel: meters_per_second_squared = 3.3

path_1 = FollowPathCustom(
    subsystem=Robot.drivetrain,
    trajectory=CustomTrajectory(
        start_pose=Pose2d(*go_back_2m[0]),
        waypoints=[Translation2d(*x) for x in go_back_2m[1]],
        end_pose=Pose2d(*go_back_2m[2]),
        max_velocity=max_vel,
        max_accel=max_accel,
        start_velocity=0,
        end_velocity=0,
    ),
    period=constants.period,
)