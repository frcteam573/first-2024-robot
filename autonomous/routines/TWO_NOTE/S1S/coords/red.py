from units.SI import meters, radians
from autonomous.routines.TWO_NOTE.S1S.coords.blue import initial, note_1, speaker
from autonomous.auto_routine import mirror_path, mirror_pose

coord = (meters, meters, radians)
waypoints = [(meters, meters)]
path = (coord, waypoints, coord)

blue_team = False

initial = mirror_pose(initial)

note_1 = mirror_path(note_1)

speaker = mirror_path(speaker)