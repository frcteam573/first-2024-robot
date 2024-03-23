import math

from autonomous.routines.FOUR_NOTE.S2S1S3S.coords.blue import (
  initial,
  note_2,
  note_3,
  note_3_short,
  note_4,
  note_4_short,
  note_2_to_speaker,
  note_3_to_speaker,
  note_4_to_speaker,
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

max_vel: meters_per_second = 2
max_accel: meters_per_second_squared = 4

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

path_1_to_speaker = FollowPathCustom(
    subsystem=Robot.drivetrain,
    trajectory=CustomTrajectory(
        start_pose=Pose2d(*note_2_to_speaker[0]),
        waypoints=[Translation2d(*x) for x in note_2_to_speaker[1]],
        end_pose=Pose2d(*note_2_to_speaker[2]),
        max_velocity=max_vel,
        max_accel=max_accel,
        start_velocity=0,
        end_velocity=0,
        rev=True,
    ),
    period=constants.period,
    blue_team=blue_team,
)

path_2_p1 = FollowPathCustom(
  subsystem=Robot.drivetrain,
  trajectory=CustomTrajectory(
    start_pose=Pose2d(*note_3_short[0]),
    waypoints=[Translation2d(*x) for x in note_3_short[1]],
    end_pose=Pose2d(*note_3_short[2]),
    max_velocity=max_vel,
    max_accel=max_accel,
    start_velocity=0,
    end_velocity=.25,
    rev=False,
  ),
  period=constants.period,
  blue_team=blue_team,
)

path_2_p2 = FollowPathCustom(
  subsystem=Robot.drivetrain,
  trajectory=CustomTrajectory(
    start_pose=Pose2d(*note_3[0]),
    waypoints=[Translation2d(*x) for x in note_3[1]],
    end_pose=Pose2d(*note_3[2]),
    max_velocity=max_vel,
    max_accel=max_accel,
    start_velocity=.25,
    end_velocity=0,
    rev=False,
  ),
  period=constants.period,
  blue_team=blue_team,
)

path_2_to_speaker = FollowPathCustom(
  subsystem=Robot.drivetrain,
  trajectory=CustomTrajectory(
    start_pose=Pose2d(*note_3_to_speaker[0]),
    waypoints=[Translation2d(*x) for x in note_3_to_speaker[1]],
    end_pose=Pose2d(*note_3_to_speaker[2]),
    max_velocity=max_vel,
    max_accel=max_accel,
    start_velocity=0,
    end_velocity=0,
    rev=True,
  ),
  period=constants.period,
  blue_team=blue_team,
)

path_3_1 = FollowPathCustom(
  subsystem=Robot.drivetrain,
  trajectory=CustomTrajectory(
    start_pose=Pose2d(*note_4_short[0]),
    waypoints=[Translation2d(*x) for x in note_4_short[1]],
    end_pose=Pose2d(*note_4_short[2]),
    max_velocity=max_vel,
    max_accel=max_accel,
    start_velocity=0,
    end_velocity=.25,
    rev=False,
  ),
  period=constants.period,
  blue_team=blue_team,
)

path_3_2 = FollowPathCustom(
  subsystem=Robot.drivetrain,
  trajectory=CustomTrajectory(
    start_pose=Pose2d(*note_4[0]),
    waypoints=[Translation2d(*x) for x in note_4[1]],
    end_pose=Pose2d(*note_4[2]),
    max_velocity=max_vel,
    max_accel=max_accel,
    start_velocity=.25,
    end_velocity=0,
    rev=False,
  ),
  period=constants.period,
  blue_team=blue_team,
)

path_3_to_speaker = FollowPathCustom(
  subsystem=Robot.drivetrain,
  trajectory=CustomTrajectory(
    start_pose=Pose2d(*note_4_to_speaker[0]),
    waypoints=[Translation2d(*x) for x in note_4_to_speaker[1]],
    end_pose=Pose2d(*note_4_to_speaker[2]),
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
  WaitCommand(0.5),
  commands.SetShoulderAngleSpeakerAuto(Robot.shoulder),
  commands.TransferNoteAuto(Robot.intake),
  commands.SetShoulderAngleAuto(Robot.shoulder, config.shoulder_floor_pos),
  ParallelDeadlineGroup( # go to note 2 to take in note
    path_1,
    commands.IntakeIn(Robot.intake),
    commands.SetShoulderAngle(Robot.shoulder, config.shoulder_floor_pos_auto),
  ),
  ParallelDeadlineGroup( # go speaker front
    path_1_to_speaker,
    commands.IntakeIn(Robot.intake),
    commands.SetShoulderAngle(Robot.shoulder, config.shoulder_front_speaker),
  ),
  commands.SetShoulderAngleSpeakerAuto(Robot.shoulder),
  commands.TransferNoteAuto(Robot.intake),
  commands.SetShoulderAngleAuto(Robot.shoulder, config.shoulder_floor_pos),
   ParallelDeadlineGroup( # go to note 2 to take in note
    path_3_1,
    commands.IntakeIn(Robot.intake),
    commands.SetShoulderAngle(Robot.shoulder, config.shoulder_floor_pos_auto),
  ),
   ParallelDeadlineGroup( # go to note 2 to take in note
    path_3_2,
    commands.IntakeIn(Robot.intake),
    commands.SetShoulderAngle(Robot.shoulder, config.shoulder_floor_pos_auto),
  ),
  ParallelDeadlineGroup( # go speaker front
    path_3_to_speaker,
    commands.IntakeIn(Robot.intake),
    commands.SetShoulderAngle(Robot.shoulder, config.shoulder_front_speaker),
  ),
  commands.SetShoulderAngleSpeakerAuto(Robot.shoulder),
  commands.TransferNoteAuto(Robot.intake),
  commands.SetShoulderAngleAuto(Robot.shoulder, config.shoulder_floor_pos),
  InstantCommand(lambda: Robot.shooter.setShooterRPM(0)),

)

routine = AutoRoutine(Pose2d(*initial), auto, blue_team=blue_team)