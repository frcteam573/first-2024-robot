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