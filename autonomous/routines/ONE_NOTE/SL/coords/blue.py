from units.SI import meters, radians
from constants import ApriltagPositionDictBlue as apb
from config import blue_scoring_positions as bsp, note_positions as np, get_perpendicular_pose, robot_length
from wpimath.geometry import Pose2d
import math

coord = (meters, meters, radians)
waypoints = [(meters, meters)]
path = (coord, waypoints, coord)

blue_team = True

pose: Pose2d = get_perpendicular_pose(Pose2d(apb[7].X(), apb[7].Y(), -math.pi/3), 0.92 + robot_length / 2, -math.pi / 3)
initial: coord = (pose.X(), pose.Y(), pose.rotation().radians())

leave: path = (
    initial,
    [(initial[0] + 0.5, initial[1] - 2)],
    (initial[0] + 2.5, initial[1] - 2.5, 0),
)