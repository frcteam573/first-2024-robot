from units.SI import meters, radians
import constants
import math
from autonomous.routines.CENTERLINE.coords.blue import initial, path_1, path_2, path_3, path_4, path_5, path_6
from autonomous.auto_routine import mirror_path, mirror_pose

coord = (meters, meters, radians)
waypoints = [(meters, meters)]
path = (coord, waypoints, coord)

blue_team = False

initial = mirror_pose(initial)

path_1 = mirror_path(path_1)

path_2 = mirror_path(path_2)

path_3 = mirror_path(path_3)

path_4 = mirror_path(path_4)

path_5 = mirror_path(path_5)

path_6 = mirror_path(path_6)