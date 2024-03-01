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
final: coord = (apb[7].X() + 1.5, apb[7].Y(), 0)

note_2: path = (
    initial,
    [],
    (np['blue_2'].X() - robot_length / 2, np['blue_2'].Y(), 0),
)

note_3: path = (
    note_2[2],
    [],
    (np['blue_1'].X(), np['blue_1'].Y(), math.pi/2),
)

speaker: path = (
    note_3[2],
    [],
    final,
)