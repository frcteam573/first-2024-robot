from units.SI import meters, radians
import constants
import math
from config import red_scoring_positions as rsp

coord = (meters, meters, radians)
waypoints = [(meters, meters)]
path = (coord, waypoints, coord)

blue_team = False

initial: coord = (0, 0, 0) # will override to robot pose

go_to_trap_2: path = (
    initial,
    [],
    (rsp['trap2'].X(), rsp['trap2'].Y(), rsp['trap2'].rotation().radians()),
)