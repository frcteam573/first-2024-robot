"""
Constant values
"""
import math

from robotpy_toolkit_7407.utils.units import hour, m, mile, rad, rev, s
from wpimath.geometry import Pose3d, Rotation3d, Transform3d

from units.SI import (
    inches_to_meters,
    meters,
    meters_per_second,
    meters_per_second_squared,
    radians,
    radians_per_second,
    rotations,
    rotations_per_minute,
    rotations_per_minute_per_second,
)

field_length = 651.25 * inches_to_meters
field_width = 323.25 * inches_to_meters

# boundary dimension constants
# --------------------------------------------------------------
horizontal_boundary: meters = (
    28 * inches_to_meters
)  # the horizontal boundary is the distance from the pivot point (center of robot) to the\
# robots maximum extension limit in the x direction (one side of the robot)
vertical_boundary: meters = (
    78 * inches_to_meters
)  # the vertical boundary is the distance from the floor to the robots maximum extension limit in the y direction
# --------------------------------------------------------------

# boundary buffer constants
# --------------------------------------------------------------
bottom_boundary_buffer_gap: meters = (
    1 * inches_to_meters
)  # the buffer in between the bottom boundary
top_boundary_buffer_gap: meters = (
    0 * inches_to_meters
)  # the buffer in between the top boundary
side_boundary_buffer_gap: meters = (
    0 * inches_to_meters
)  # the buffer in between the side boundaries
# --------------------------------------------------------------

# shoulder constants
# --------------------------------------------------------------
shoulder_max_rotation: radians = math.radians(
    80
)  # the maximum rotation of the shoulder
shoulder_min_rotation: radians = math.radians(
    110
)  # the minimum rotation of the shoulder
shoulder_intake_up_max_rotation: radians = math.radians(
    90
)  # the maximum rotation of the shoulder when the intake is up
# --------------------------------------------------------------

# shoulder buffer constants
# --------------------------------------------------------------
shoulder_min_buffer_rotation: radians = math.radians(
    1
)  # the buffer in between the minimum rotation
shoulder_max_buffer_rotation: radians = math.radians(
    1
)  # the buffer in between the maximum rotation
# --------------------------------------------------------------

# elevator constants
# --------------------------------------------------------------
min_elevator_height: meters = (
    30 * inches_to_meters
)  # the minimum height of the elevator
elevator_pivot_offset: meters = (
    -2.5 * inches_to_meters
)  # offset from the pivot point to the center of the elevator
max_elevator_height: meters = (
    59.5 * inches_to_meters
)  # the maximum height of the elevator
max_elevator_height_delta: meters = (
    40 * inches_to_meters
)  # the maximum height of the elevator
pivot_point_height: meters = 17 * inches_to_meters  # the height of the pivot point
# --------------------------------------------------------------

# --------------------------------------------------------------
elevator_zero_length: meters = (min_elevator_height / 2) + (-elevator_pivot_offset)
# gets the length of the elevator above the pivot point using the offset and the min height
# --------------------------------------------------------------

# arm pose accuracy
# --------------------------------------------------------------
arm_pose_accuracy: float = 0.01  # the accuracy of the arm pose
# --------------------------------------------------------------

# claw constants
# --------------------------------------------------------------
claw_height: meters = 10 * inches_to_meters  # the height of the claw
claw_width: meters = 3 * inches_to_meters  # the width of the claw
claw_length_open: meters = (
    14 * inches_to_meters
)  # the length of the claw when it is open
claw_length_close: meters = (
    8 * inches_to_meters
)  # the length of the claw when it is closed
# --------------------------------------------------------------


# elevator gear ratios
# --------------------------------------------------------------
elevator_rotation_gear_ratio: rotations = 67.38  # to one
elevator_extend_gear_ratio: rotations = 6.33  # 6.33  # to one
elevator_length_per_rotation: meters = (
    1.736 * inches_to_meters
)  # the length of the elevator per rotation
wrist_gear_ratio: rotations = 80
# 24 rotations to max extension
stabilizer_magnitude: float = (
    2  # the magnitude of the rotation of the arm based on the tip of the robot
)
shoulder_max_velocity: rotations_per_minute = 25 * elevator_rotation_gear_ratio  # RPM
shoulder_max_acceleration: rotations_per_minute_per_second = (
    25 * elevator_rotation_gear_ratio
)  # RPM / S
shoulder_min_acceleration: rotations_per_minute_per_second = (
    5 * elevator_extend_gear_ratio
)  # RPM / S
# --------------------------------------------------------------


# Wrist soft mount
# --------------------------------------------------------------
wrist_max_rotation: radians = math.radians(90)  # the maximum rotation of the wrist
wrist_min_rotation: radians = math.radians(90)  # the minimum rotation of the wrist
# --------------------------------------------------------------

# elevator zeroing constants
# --------------------------------------------------------------
elevator_initial_rotation = (
    0  # the initial rotation of the elevator that it will zero to
)
elevator_initial_length = (
    0 * inches_to_meters
)  # the initial length of the elevator that it will zero to
# --------------------------------------------------------------

claw_motor_speed: float = 0.2
# --------------------------------------------------------------

period = 0.03

# --- DRIVETRAIN ---
# drivetrain_turn_gear_ratio = ((8.16 * 4096)/(2*math.pi) * rev_sensor_unit / rad).asNumber()

drivetrain_turn_gear_ratio: rotations = 9424/203  # 46.42 #Updated for 3in Rev Swerve
drivetrain_move_gear_ratio_as_rotations_per_meter = 1 / (((3 * math.pi) / 3.75) * inches_to_meters) #Updated for 3in Rev Swerve

drivetrain_move_gear_ratio: rotations_per_minute = (
    drivetrain_move_gear_ratio_as_rotations_per_meter * 60
)

track_width: meters = 25.5 * inches_to_meters
# robot_length: meters = 35.5 * inches_to_meters

# TODO Maybe change these
drivetrain_accel = True
drivetrain_max_vel: meters_per_second = (13 * mile / hour).asNumber(m / s)  # 12
drivetrain_max_accel_tele: meters_per_second_squared = (45 * mile / hour).asNumber(m / s)
drivetrain_max_target_accel: meters_per_second_squared = (
    45 * mile / hour
).asNumber(  # 10
    m / s
)
drivetrain_target_max_vel: meters_per_second = (3 * mile / hour).asNumber(m / s)  # 12
drivetrain_max_angular_vel: radians_per_second = (1 * rev / s).asNumber(rad / s)  # 1
drivetrain_max_correction_vel: radians_per_second = (2 * rev / s).asNumber(rad / s)
drivetrain_max_climb_vel: meters_per_second = (5 * mile / hour).asNumber(m / s)

climber_out = False
# this sets up the operator controller to determine which state the climber is in at the start of the match :)

ApriltagPositionDictRed = {
    3: Pose3d(
        (field_length / 2 + 8.308467),
        (field_width / 2 + 0.877443),
        (1.451102),
        Rotation3d(0.0, 0.0, math.pi),
    ),
    4: Pose3d(
        (field_length / 2 + 8.308467),
        (field_width / 2 + 1.442593),
        (1.451102),
        Rotation3d(0.0, 0.0, math.pi),
    ),
    5: Pose3d(
        (field_length / 2 + 6.429883),
        (field_width / 2 + 4.098925),
        (1.355852),
        Rotation3d(0.0, 0.0, -math.pi / 2),
    ),
    9: Pose3d(
        (field_length / 2 + -7.914767),
        (field_width / 2 + -3.221609),
        (1.355852),
        Rotation3d(0.0, 0.0, math.pi / 3),
    ),
    10: Pose3d(
        (field_length / 2 + -6.809359),
        (field_width / 2 + -3.859403),
        (1.355852),
        Rotation3d(0.0, 0.0, math.pi / 3),
    ),
    11: Pose3d(
        (field_length / 2 + 3.633851),
        (field_width / 2 + -0.392049),
        (1.3208),
        Rotation3d(0.0, 0.0, -math.pi / 6),
    ),
    12: Pose3d(
        (field_length / 2 + 3.633851),
        (field_width / 2 + 0.393065),
        (1.3208),
        Rotation3d(0.0, 0.0, math.pi / 6),
    ),
    13: Pose3d(
        (field_length / 2 + 2.949321),
        (field_width / 2 + -0.000127),
        (1.3208),
        Rotation3d(0.0, 0.0, math.pi),
    ),
}

ApriltagPositionDictBlue = {
    1: Pose3d(
        (field_length / 2 + 6.808597),
        (field_width / 2 + -3.859403),
        (1.355852),
        Rotation3d(0.0, 0.0, 2 * math.pi / 3),
    ),
    2: Pose3d(
        (field_length / 2 + 7.914259),
        (field_width / 2 + -3.221609),
        (1.355852),
        Rotation3d(0.0, 0.0, 2 * math.pi / 3),
    ),
    6: Pose3d(
        (field_length / 2 + -6.429375),
        (field_width / 2 + 4.098925),
        (1.355852),
        Rotation3d(0.0, 0.0, -math.pi / 2),
    ),
    7: Pose3d(
        (field_length / 2 + -8.308975),
        (field_width / 2 + 1.442593),
        (1.451102),
        Rotation3d(0.0, 0.0, 0),
    ),
    8: Pose3d(
        (field_length / 2 + -8.308975),
        (field_width / 2 + 0.877443),
        (1.451102),
        Rotation3d(0.0, 0.0, 0),
    ),
    14: Pose3d(
        (field_length / 2 + -2.950083),
        (field_width / 2 + -0.000127),
        (1.3208),
        Rotation3d(0.0, 0.0, 0),
    ),
    15: Pose3d(
        (field_length / 2 + -3.629533),
        (field_width / 2 + 0.393065),
        (1.3208),
        Rotation3d(0.0, 0.0,  2 * math.pi / 3),
    ),
    16: Pose3d(
        (field_length / 2 + -3.629533),
        (field_width / 2 + -0.392049),
        (1.3208),
        Rotation3d(0.0, 0.0,  -2 * math.pi / 3),
    ),
}

kCameras = {
    "Arducam_OV9281_USB_Camera": [
        Transform3d(
            Pose3d(),
            Pose3d(
                6.43 * inches_to_meters,
                -7 * inches_to_meters,
                22.5 * inches_to_meters,
                Rotation3d(0, 0, math.radians(180)),
            ),
        )
    ],
    "Arducam_OV9281_USB_Camera_2": [
        Transform3d(
            Pose3d(),
            Pose3d(
                -6.43 * inches_to_meters,
                -7 * inches_to_meters,
                22.5 * inches_to_meters,
                Rotation3d(0, 0, math.radians(0)),
            ),
        )
    ],
}

# Climber:

climber_motor_gear_ratio = 16
climber_pivot_rotations = 1.22 * climber_motor_gear_ratio
climber_unlatch_extension = 0.3 * climber_motor_gear_ratio