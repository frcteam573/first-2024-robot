from units.SI import meters, radians
from autonomous.routines.THREE_NOTE.S2S3S.coords.blue import initial, note_2, note_2_to_speaker, note_3, speaker
from autonomous.auto_routine import mirror_path, mirror_pose
import constants
import math

coord = (meters, meters, radians)
waypoints = [(meters, meters)]
path = (coord, waypoints, coord)

blue_team = False

initial = mirror_pose(initial)

note_2 = mirror_path(note_2)

note_2_to_speaker = mirror_path(note_2_to_speaker)

note_3 = mirror_path(note_3)

speaker = mirror_path(speaker)