import math

from autonomous.routines.ONE_NOTE.SB.coords.blue import (
  initial,
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
import commands.autonomous.collections as collections
from commands.autonomous.custom_pathing import FollowPathCustom, FollowPathCustomAprilTag
from commands.autonomous.trajectory import CustomTrajectory
from autonomous.auto_routine import AutoRoutine
from robot_systems import Robot, Sensors
from units.SI import meters_per_second, meters_per_second_squared

max_vel: meters_per_second = 1.3
max_accel: meters_per_second_squared = 3

auto = SequentialCommandGroup(
  collections.AlignAndShoot(),
)

routine = AutoRoutine(Pose2d(*initial), auto, blue_team=blue_team)