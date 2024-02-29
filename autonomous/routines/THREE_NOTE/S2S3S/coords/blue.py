from units.SI import meters, radians
from constants import ApriltagPositionDictBlue as apb
from config import blue_scoring_positions as bsp, note_positions as np
import math

coord = (meters, meters, radians)
waypoints = [(meters, meters)]
path = (coord, waypoints, coord)

blue_team = True

initial: coord = (apb[7].X() + 1.2954, apb[7].Y(), 0)

note_2: path = (
    initial,
    [],
    (np['blue_2'].X(), np['blue_2'].Y(), 0),
)

note_3: path = (
    note_2[2],
    [],
    (np['blue_3'].X(), np['blue_3'].Y(), -math.pi / 2),
)

speaker: path = (
    note_3[2],
    [],
    (np['blue_3'].X() - 1, np['blue_3'].Y() + 1, -math.pi / 6),
)