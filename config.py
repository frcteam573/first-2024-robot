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

Shoulder_Floor_Pos = 1.7 # Need to verify this is a guess
Shoulder_Amp_Pos = .4 # Need to verify this is a guess
Shoulder_Human_Pos = 1.3 # Need to verify this is a guess
Shoulder_Trap_Pos = 1.3 # Need to verify this is a guess

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

# Climber Configurations:
# Needs to be verified

climber_motor_id = 7

compressor = 31
climber_forwardChannel = 11
climber_reverseChannel = 10

latch_forwardChannel = 8
latch_reverseChannel = 9

current_scoring_position = "None"

intake_inverted = False

grabber_target_angle = 0
grabber_disable_intake = False

blue_team: bool = False
drivetrain_reversed: bool = False
driver_centric: bool = True

scoring_width = 216.2 * inches_to_meters  # 5.44

drivetrain_scoring_velocity = 0.5
drivetrain_scoring_angular_velocity = 1
drivetrain_routing_velocity = 2
drivetrain_routing_acceleration = 1
drivetrain_routing_angular_velocity = 3


@dataclass
class TargetData:
    arm_angle: radians
    arm_length: meters
    wrist_angle: radians
    target_pose: Pose2d | None
    target_waypoints: list[Translation2d] = None
    intake_enabled: bool = False
    intake_reversed: bool = False
    intake_off: bool = False

    claw_picking: bool = False
    cube_picking: bool = False
    cone_picking: bool = False
    double_station_picking: bool = False

    claw_scoring: bool = False
    arm_scoring: bool = False
    arm_reversed: bool = False

    claw_wait: bool = False

    max_velocity: meters_per_second = None
    max_acceleration: meters_per_second_squared = None
    max_angular_velocity: meters_per_second = None

    grabber_no_grab: bool = False

    low_scoring: bool = False
    arm_angle_opposite: float | None = None
    arm_length_opposite: float | None = None
    wrist_angle_opposite: float | None = None

    no_intake: bool = False


elevator_motor_extend_id = 17
elevator_secondary_rotation_motor_id = 1
elevator_main_rotation_motor_id = 2
elevator_brake_id = 3
# converted to radians in subsystems/elevator.py

pneumatics_control_module = 31

claw_motor_speed: float = 0.6

# Intake
intake_motor_id = 11
intake_piston_forwardChannel = 4
intake_piston_reverseChannel = 5

default_intake_speed = 0.40

kRobotVisionPoseWeight = 0.1
# Dummy data
claw_motor_extend_id = 0

# shoulder positions (degrees)
shoulder_floor = 0
shoulder_amp = 0
shoulder_human = 0
shoulder_trap = 0
shoulder_home = 0

shoulder_min = 0
shoulder_max = 100


# speed/alignment thresholds
vision_threshold = 3    # degrees
shooter_threshold = .05 # percent
shoulder_threshold = math.pi/60  # degrees

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

# SCORING LOCATIONS
scoring_locations: dict[str, TargetData] = {
    "low": TargetData(
        target_pose=None,
        arm_angle=math.radians(-98),
        arm_length=0,
        wrist_angle=math.radians(0),
        arm_angle_opposite=math.radians(50),
        arm_length_opposite=0.2,
        wrist_angle_opposite=math.radians(90),
        intake_enabled=False,
        claw_scoring=False,
        claw_picking=False,
        cone_picking=False,
        low_scoring=True,
        arm_scoring=True,
    ),
    "middle": TargetData(
        target_pose=Pose2d(1.55, 1.55, 0),  # 2.43 .94
        target_waypoints=[Translation2d(1.81, 1.55)],
        arm_angle=math.radians(-53.78),
        arm_length=0.55,
        wrist_angle=math.radians(-27.09),
        intake_enabled=False,
        claw_scoring=True,
        claw_picking=False,
        arm_scoring=True,
        max_velocity=1,
        max_acceleration=0.5,
        max_angular_velocity=1,
        claw_wait=True,
    ),
    "high": TargetData(
        target_pose=None,
        arm_angle=math.radians(-49.7),
        arm_length=1.01,
        wrist_angle=math.radians(25),
        intake_enabled=False,
        claw_scoring=True,
        claw_picking=False,
        arm_scoring=True,
        max_velocity=1,
        max_acceleration=0.5,
        max_angular_velocity=1,
        claw_wait=True,
    ),
    "high_auto_back": TargetData(
        target_pose=None,
        arm_angle=math.radians(-49.7),
        arm_length=1.01,
        wrist_angle=math.radians(-25),
        intake_enabled=False,
        claw_scoring=False,
        claw_picking=False,
        arm_scoring=False,
        max_velocity=1,
        max_acceleration=0.5,
        max_angular_velocity=1,
        claw_wait=True,
    ),
    "high_auto_back_intake": TargetData(
        target_pose=None,
        arm_angle=math.radians(-49.7),
        arm_length=1.01,
        wrist_angle=math.radians(-25),
        intake_enabled=True,
        claw_scoring=False,
        claw_picking=False,
        arm_scoring=False,
        max_velocity=1,
        max_acceleration=0.5,
        max_angular_velocity=1,
        claw_wait=True,
    ),
    "high_auto_back_cube": TargetData(
        target_pose=None,
        arm_angle=math.radians(-49.7),
        arm_length=1.01,
        wrist_angle=math.radians(-30),
        intake_enabled=False,
        claw_scoring=False,
        claw_picking=False,
        arm_scoring=False,
        max_velocity=1,
        max_acceleration=0.5,
        max_angular_velocity=1,
    ),
    "mid_auto_back_cube": TargetData(
        target_pose=None,
        arm_angle=math.radians(-64),
        arm_length=0.55,
        wrist_angle=math.radians(-24.09),
        intake_enabled=False,
        claw_scoring=False,
        claw_picking=False,
        arm_scoring=False,
        max_velocity=1,
        max_acceleration=0.5,
        max_angular_velocity=1,
    ),
    "middle_auto_back": TargetData(
        target_pose=None,
        arm_angle=math.radians(-64),
        arm_length=0.55,
        wrist_angle=math.radians(-24.09),
        intake_enabled=False,
        claw_scoring=False,
        claw_picking=False,
        arm_scoring=False,
        max_velocity=1,
        max_acceleration=0.5,
        max_angular_velocity=1,
        claw_wait=False,
    ),
    "middle_auto_front": TargetData(
        target_pose=None,
        arm_angle=math.radians(46.78),
        arm_length=0.55,
        wrist_angle=math.radians(27.09),
        intake_enabled=False,
        claw_scoring=False,
        claw_picking=False,
        arm_scoring=False,
        max_velocity=1,
        max_acceleration=0.5,
        max_angular_velocity=1,
        claw_wait=False,
    ),
    "pickup": TargetData(
        target_pose=None,
        arm_angle=math.radians(-108),
        arm_length=0.199,
        wrist_angle=math.radians(-10),
        intake_enabled=False,
        claw_scoring=False,
        claw_picking=True,
        cone_picking=True,
    ),
    "double_station": TargetData(
        target_pose=Pose2d(16, 7.51, math.radians(0)),
        arm_angle=math.radians(32.84),
        arm_length=0.350,  # .322 for comp
        wrist_angle=math.radians(54.63),
        intake_enabled=False,
        claw_scoring=False,
        claw_picking=True,
        arm_scoring=True,
        arm_reversed=True,
        double_station_picking=True,
    ),
    "cube_intake": TargetData(
        target_pose=None,
        arm_angle=math.radians(74.5),
        arm_length=2.5 * units.SI.inches_to_meters,
        wrist_angle=math.radians(100),
        intake_enabled=True,
        claw_scoring=False,
        claw_picking=True,
        cube_picking=True,
    ),
    "cube_intake_off": TargetData(
        target_pose=None,
        arm_angle=math.radians(74.5),
        arm_length=0 * units.SI.inches_to_meters,
        wrist_angle=math.radians(100),
        intake_enabled=True,
        claw_scoring=False,
        claw_picking=True,
        cube_picking=True,
        intake_off=True,
    ),
    "cube_intake_no_grab": TargetData(
        target_pose=None,
        arm_angle=math.radians(0),
        arm_length=0 * units.SI.inches_to_meters,
        wrist_angle=math.radians(0),
        intake_enabled=True,
        claw_scoring=False,
        claw_picking=False,
        cube_picking=False,
        grabber_no_grab=False,
        no_intake=False,
    ),
    "cube_intake_auto_but_slightly_higher": TargetData(
        target_pose=None,
        arm_angle=math.radians(54.5),
        arm_length=0 * units.SI.inches_to_meters,
        wrist_angle=math.radians(100),
        intake_enabled=True,
        claw_scoring=False,
        claw_picking=True,
    ),
    "cube_intake_auto": TargetData(
        target_pose=None,
        arm_angle=math.radians(74.5),
        arm_length=1 * units.SI.inches_to_meters,
        wrist_angle=math.radians(100),
        intake_enabled=True,
        claw_scoring=False,
        claw_picking=True,
    ),
    "cube_intake_auto_2": TargetData(
        target_pose=None,
        arm_angle=math.radians(74.5),
        arm_length=0 * units.SI.inches_to_meters,
        wrist_angle=math.radians(100),
        intake_enabled=True,
        claw_scoring=False,
        claw_picking=True,
        intake_off=True,
    ),
    "standard": TargetData(
        target_pose=None,
        arm_angle=math.radians(0),
        arm_length=0,
        wrist_angle=math.radians(0),
        intake_enabled=False,
        claw_scoring=False,
        claw_picking=False,
    ),
    "standard_pickup": TargetData(
        target_pose=None,
        arm_angle=math.radians(0),
        arm_length=0,
        wrist_angle=math.radians(0),
        intake_enabled=False,
        claw_scoring=False,
        claw_picking=False,
        claw_wait=True,
    ),
    "eject": TargetData(
        target_pose=None,
        arm_angle=math.radians(-45),
        arm_length=0,
        wrist_angle=math.radians(0),
        intake_enabled=True,
        claw_scoring=False,
        claw_picking=False,
        claw_wait=False,
        intake_reversed=True,
    ),
}