from units.SI import meters, radians
import constants
import math
from autonomous.routines.TWO_NOTE.SC5S.coords.blue import initial, note_c5, speaker
from autonomous.auto_routine import mirror_path, mirror_pose

coord = (meters, meters, radians)
waypoints = [(meters, meters)]
path = (coord, waypoints, coord)

blue_team = False

initial = mirror_pose(initial)

note_c5 = mirror_path(note_c5)

speaker = mirror_path(speaker)