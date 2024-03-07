from units.SI import meters, radians
from constants import ApriltagPositionDictBlue as apb
from config import blue_scoring_positions as bsp, note_positions as np, robot_length
import math

coord = (meters, meters, radians)
waypoints = [(meters, meters)]
path = (coord, waypoints, coord)

blue_team = True

initial: coord = (apb[7].X() + 0.918 + robot_length / 2, apb[7].Y(), 0)

note_2: path = (
    initial,
    [],
    (np['blue_2'].X() - robot_length / 2, np['blue_2'].Y(), 0),
)

speaker: path = (
    note_2[2],
    [],
    initial,
)

