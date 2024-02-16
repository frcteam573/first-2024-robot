from units.SI import meters, radians
from constants import ApriltagPositionDictBlue as apb
from config import blue_scoring_positions as bsp, note_positions as np
import math

coord = (meters, meters, radians)
waypoints = [(meters, meters)]
path = (coord, waypoints, coord)

blue_team = True

initial: coord = (apb[7].X() + 1.2954, apb[7].Y(), math.pi)

note_2: path = (
    initial,
    [],
    (np['blue_2'].X(), np['blue_2'].Y(), math.pi),
)

amp: path = (
    note_2[2],
    [],
    (bsp['amp'].X(), bsp['amp'].Y(), bsp['amp'].rotation()),
)

note_1: path = (
    amp[2],
    [],
    (np['blue_1'].X() - 1, np['blue_1'].Y() + 1, 5 * math.pi / 6),
)

amp: path = (
    note_1[2],
    [],
    (bsp['amp'].X(), bsp['amp'].Y(), bsp['amp'].rotation()),
)