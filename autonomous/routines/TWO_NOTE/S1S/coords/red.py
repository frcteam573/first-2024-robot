from units.SI import meters, radians
from autonomous.routines.TWO_NOTE.S1S.coords.blue import initial, note_1, speaker, note_c1, speaker_2
from autonomous.auto_routine import mirror_path, mirror_pose

coord = (meters, meters, radians)
waypoints = [(meters, meters)]
path = (coord, waypoints, coord)

blue_team = False

initial = mirror_pose(initial)

note_1 = mirror_path(note_1)

speaker = mirror_path(speaker)

note_c1 = mirror_path(note_c1)

speaker_2 = mirror_path(speaker_2)