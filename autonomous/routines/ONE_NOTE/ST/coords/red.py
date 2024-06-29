from units.SI import meters, radians
from autonomous.routines.ONE_NOTE.ST.coords.blue import initial
from autonomous.auto_routine import mirror_path, mirror_pose

coord = (meters, meters, radians)
waypoints = [(meters, meters)]
path = (coord, waypoints, coord)

blue_team = False

initial = mirror_pose(initial)