from units.SI import meters, radians
from autonomous.routines.TWO_NOTE.S2S.coords.blue import initial, note_2
from autonomous.auto_routine import mirror_path, mirror_pose

coord = (meters, meters, radians)
waypoints = [(meters, meters)]
path = (coord, waypoints, coord)

blue_team = False

initial = mirror_pose(initial)

note_2 = mirror_path(note_2)