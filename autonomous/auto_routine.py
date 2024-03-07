from dataclasses import dataclass
from constants import field_length

import commands2
from commands2 import CommandBase
from wpimath.geometry import Pose2d

from robot_systems import Robot
import commands
import math

def mirror_waypoints(waypoints):
    """
    Mirrors a list of waypoints across the y-axis.
    """
    return [(field_length - x, y) for x, y in waypoints]

def mirror_pose(pose):
    """
    Mirrors a pose across the y-axis.
    """
    return (field_length - pose[0], pose[1], -pose[2] + math.pi)

def mirror_path(path):
    """
    Mirrors a path across the y-axis.
    """
    start, waypoints, end = path
    return [
        mirror_pose(start),
        mirror_waypoints(waypoints),
        mirror_pose(end)
    ]

@dataclass
class AutoRoutine:
    """
    Base auto-routine class.

    :param initial_robot_pose: Initial robot pose.
    :type initial_robot_pose: Pose2d
    :param command: Command to run.
    :type command: CommandBase
    """

    initial_robot_pose: Pose2d
    command: CommandBase
    blue_team: bool = True

    def run(self):
        """
        Runs the autonomous routine
        """
        # commented this out because i want robot paths from current position, lets see if it still works
        Robot.drivetrain.gyro.reset_angle(self.initial_robot_pose.rotation().radians())
        Robot.drivetrain.reset_odometry(self.initial_robot_pose)

        commands2.CommandScheduler.getInstance().schedule(self.command)
        # print("running path for " + "blue" if self.blue_team else "red" + " team")

    def end():
        commands2.CommandScheduler.getInstance().schedule(
            commands.DriveSwerveCustom(Robot.drivetrain)
        )
        
@dataclass
class TeleRoutine:
    """
    Base auto-routine class.

    :type initial_robot_pose: Pose2d
    :param command: Command to run.
    :type command: CommandBase
    """

    command: CommandBase
    blue_team: bool = True

    def run(self):
        """
        Runs the teleop routine
        """

        commands2.CommandScheduler.getInstance().schedule(self.command)
        # print("running path for " + "blue" if self.blue_team else "red" + " team")

    def end():
        commands2.CommandScheduler.getInstance().schedule(
            commands.DriveSwerveCustom(Robot.drivetrain)
        )