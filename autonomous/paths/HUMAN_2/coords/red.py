from units.SI import meters, radians
import constants
import math
from config import red_scoring_positions as rsp

coord = (meters, meters, radians)
waypoints = [(meters, meters)]
path = (coord, waypoints, coord)

blue_team = False

initial: coord = (0, 0, 0) # will override to robot pose

go_to_human_2: path = (
    initial,
    [],
    (rsp['human2'].X(), rsp['human2'].Y(), rsp['human2'].rotation().radians()),
)