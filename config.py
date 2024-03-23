import math
from dataclasses import dataclass

from wpimath.geometry import Pose2d,Rotation2d, Translation2d, Transform2d

import units.SI
from units.SI import (
    inches_to_meters,
    meters,
    meters_per_second,
    meters_per_second_squared,
    radians,
)
from constants import ApriltagPositionDictBlue as ATPosesBlue, ApriltagPositionDictRed as ATPosesRed
from constants import field_length, field_width

robot_length = 35.5 * inches_to_meters
robot_width = 35.5 * inches_to_meters

shoulder_floor_pos = 1.44
shoulder_floor_pos_auto = 1.44
shoulder_mid_pos = 0.7
shoulder_amp_pos = 0
shoulder_human_pos = .436
shoulder_trap_pos = .145

shoulder_front_speaker = 0.9

def get_perpendicular_pose(pose: Pose2d, distance: float, new_angle: float) -> Pose2d:
    new_pose = Pose2d(
        Translation2d(
            pose.X() + (distance * math.cos(pose.rotation().radians())),
            pose.Y() + (distance * math.sin(pose.rotation().radians())),
        ),
        Rotation2d(new_angle),
    )

    return new_pose

def get_average_pose(pose1: Pose2d, pose2: Pose2d) -> Pose2d:
    return Pose2d(
        Translation2d(
            (pose1.X() + pose2.X()) / 2,
            (pose1.Y() + pose2.Y()) / 2,
        ),
        Rotation2d(
            (pose1.rotation().radians() + pose2.rotation().radians()) / 2
        ),
    )

blue_team: bool = False
drivetrain_reversed: bool = False
driver_centric: bool = True

scoring_width = 216.2 * inches_to_meters  # 5.44

drivetrain_scoring_velocity = 0.5
drivetrain_scoring_angular_velocity = 1
drivetrain_routing_velocity = 2
drivetrain_routing_acceleration = 1
drivetrain_routing_angular_velocity = 3

shoulder_min = 0
shoulder_max = 100


# speed/alignment thresholds
vision_threshold = 3    # degrees
shooter_threshold = .05 # percent
shoulder_threshold = 0.05 #radians
shoulder_threshold_lowest = .03  # radians .025
shoulder_threshold_lowest_distance = 72 * inches_to_meters  # m
shoulder_threshold_highest = .07  # radians .025
shoulder_threshold_highest_distance = 36 * inches_to_meters  # m



blue_scoring_positions = {
    'amp': Pose2d(ATPosesBlue[6].X(), ATPosesBlue[6].Y() - 0.7, -math.pi / 2),
    'human1': get_perpendicular_pose(ATPosesBlue[1].toPose2d(), .7, ATPosesBlue[1].rotation().Z() + math.pi),
    'human2': get_perpendicular_pose(get_average_pose(ATPosesBlue[1].toPose2d(), ATPosesBlue[2].toPose2d()), .7, ATPosesBlue[1].rotation().Z() + math.pi),
    'human3': get_perpendicular_pose(ATPosesBlue[2].toPose2d(), .7, ATPosesBlue[2].rotation().Z() + math.pi),
    'trap1': get_perpendicular_pose(ATPosesBlue[14].toPose2d(), 2, ATPosesBlue[14].rotation().Z() + math.pi),
    'trap2': get_perpendicular_pose(ATPosesBlue[15].toPose2d(), 2, ATPosesBlue[15].rotation().Z() + math.pi),
    'trap3': get_perpendicular_pose(ATPosesBlue[16].toPose2d(), 2, ATPosesBlue[16].rotation().Z() + math.pi)
}

red_scoring_positions = {
    'amp': Pose2d(ATPosesRed[5].X(), ATPosesRed[5].Y() - 0.7, -math.pi / 2),
    'human1': get_perpendicular_pose(ATPosesRed[10].toPose2d(), .7, ATPosesRed[10].rotation().Z() + math.pi),
    'human2': get_perpendicular_pose(get_average_pose(ATPosesRed[10].toPose2d(), ATPosesRed[9].toPose2d()), .7, ATPosesRed[10].rotation().Z() + math.pi),
    'human3': get_perpendicular_pose(ATPosesRed[9].toPose2d(), .7, ATPosesRed[9].rotation().Z() + math.pi),
    'trap1': get_perpendicular_pose(ATPosesRed[13].toPose2d(), 2, ATPosesRed[13].rotation().Z() + math.pi),
    'trap2': get_perpendicular_pose(ATPosesRed[12].toPose2d(), 2, ATPosesRed[12].rotation().Z() + math.pi),
    'trap3': get_perpendicular_pose(ATPosesRed[11].toPose2d(), 2, ATPosesRed[11].rotation().Z() + math.pi)
}

note_positions = {
    'blue_1': Pose2d(120 * inches_to_meters, field_width / 2 + 114 * inches_to_meters, 0),
    'blue_2': Pose2d(120 * inches_to_meters, field_width / 2 + 57 * inches_to_meters, 0),
    'blue_3': Pose2d(120 * inches_to_meters, field_width / 2, 0),
    'center_1': Pose2d(field_length / 2, field_width / 2 + 132 * inches_to_meters, 0),
    'center_2': Pose2d(field_length / 2, field_width / 2 + 66 * inches_to_meters, 0),
    'center_3': Pose2d(field_length / 2, field_width / 2, 0),
    'center_4': Pose2d(field_length / 2, field_width / 2 - 66 * inches_to_meters, 0),
    'center_5': Pose2d(field_length / 2, field_width / 2 - 132 * inches_to_meters, 0),
    'red_1': Pose2d(field_length - 120 * inches_to_meters, field_width / 2 + 114 * inches_to_meters, 0),
    'red_2': Pose2d(field_length - 120 * inches_to_meters, field_width / 2 + 57 * inches_to_meters, 0),
    'red_3': Pose2d(field_length - 120 * inches_to_meters, field_width / 2, 0),
}