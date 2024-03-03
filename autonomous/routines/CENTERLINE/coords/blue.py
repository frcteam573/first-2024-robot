from units.SI import meters, radians
from constants import ApriltagPositionDictBlue as apb
from config import blue_scoring_positions as bsp, note_positions as np, get_perpendicular_pose, robot_length
from wpimath.geometry import Pose2d
import math

coord = (meters, meters, radians)
waypoints = [(meters, meters)]
path = (coord, waypoints, coord)

blue_team = True

# pose: Pose2d = get_perpendicular_pose(Pose2d(apb[7].X(), apb[7].Y(), -math.pi/3), 0.918 + robot_length / 2, -math.pi / 3)
initial: coord = (robot_length / 2, 2.05, 0)
shoot_loc: coord = (robot_length/2 + 4, 2, -math.pi/6)

path_1: path = (
    initial,
    [],
    (np['center_5'].X() - robot_length / 2, np['center_5'].Y(), 0),
)

path_2: path = (
    path_1[2],
    [],
    shoot_loc,
)

path_3: path = (
    shoot_loc,
    [],
    (np['center_4'].X() - robot_length / 2, np['center_4'].Y(), 0),
)

path_4: path = (
    path_3[2],
    [],
    shoot_loc,
)

path_5: path = (
    shoot_loc,
    [],
    (np['center_3'].X(), np['center_3'].Y() - robot_length/2, math.pi/2),
)

path_6: path = (
    path_5[2],
    [],
    shoot_loc,
)