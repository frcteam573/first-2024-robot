from units.SI import meters, radians
import constants
import math
from autonomous.routines.ONE_NOTE.SL.coords.blue import initial, leave
from autonomous.auto_routine import mirror_path, mirror_pose

coord = (meters, meters, radians)
waypoints = [(meters, meters)]
path = (coord, waypoints, coord)

blue_team = False

initial = mirror_pose(initial)

leave = mirror_path(leave)