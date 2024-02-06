from units.SI import meters, radians
import constants
import math
from config import blue_scoring_positions as bsp

coord = (meters, meters, radians)
waypoints = [(meters, meters)]
path = (coord, waypoints, coord)

blue_team = True

initial: coord = (0, 0, 0) # will override to robot pose

go_to_amp: path = (
    initial,
    [],
    (bsp['amp'].X(), bsp['amp'].Y(), bsp['amp'].rotation().radians()),
)