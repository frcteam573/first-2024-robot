from units.SI import meters, radians
from constants import ApriltagPositionDictBlue as apb
from config import blue_scoring_positions as bsp, note_positions as np, get_perpendicular_pose, robot_length
from wpimath.geometry import Pose2d
import math

coord = (meters, meters, radians)
waypoints = [(meters, meters)]
path = (coord, waypoints, coord)

blue_team = True

initial: coord = (apb[7].X() + 0.918 + robot_length / 2, apb[7].Y(), 0)
speaker_front: coord = (apb[7].X() + 1.5, apb[7].Y(), 0)

note_2: path = (
    initial,
    [],
    (np['blue_2'].X() - robot_length / 2, np['blue_2'].Y(), 0),
)

note_2_to_speaker: path = (
    note_2[2],
    [],
    speaker_front,
)

note_3_short: path = (
    speaker_front,
    [],
    (np['blue_1'].X()- robot_length/2 - .5, np['blue_1'].Y(), 0),
)

note_3: path = (
    note_3_short[2],
    [],
    (np['blue_1'].X()- robot_length / 2, np['blue_1'].Y(), 0),
)

note_3_to_speaker: path = (
    note_3[2],
    [],
    speaker_front,
)

note_4_short: path = (
    speaker_front,
    [],
    (np['blue_3'].X()- robot_length / 2 - .5, np['blue_3'].Y(), 0),
)

note_4: path = (
    note_4_short[2],
    [],
    (np['blue_3'].X()- robot_length / 2, np['blue_3'].Y(), 0),
)


note_4_to_speaker: path = (
    note_4[2],
    [],
    speaker_front,
)