from units.SI import meters, radians
from constants import ApriltagPositionDictBlue as apb
from config import blue_scoring_positions as bsp, note_positions as np
import math

coord = (meters, meters, radians)
waypoints = [(meters, meters)]
path = (coord, waypoints, coord)

blue_team = True

initial: coord = (apb[7].X() + 1.2954, apb[7].Y(), math.pi)

note_3: path = (
    initial,
    [],
    (np['blue_3'].X(), np['blue_3'].Y(), math.pi),
)

note_1: path = (
    note_3[2],
    [],
    (np['blue_1'].X(), np['blue_1'].Y(), math.pi / 2),
)

amp: path = (
    note_1[2],
    [],
    (bsp['amp'].X(), bsp['amp'].Y(), bsp['amp'].rotation()),
)