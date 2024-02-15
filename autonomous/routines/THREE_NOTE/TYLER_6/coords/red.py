from units.SI import meters, radians
import constants
import math

coord = (meters, meters, radians)
waypoints = [(meters, meters)]
path = (coord, waypoints, coord)

blue_team = False

initial: coord = (constants.ApriltagPositionDictRed[4].X() - 1.2954, constants.ApriltagPositionDictRed[4].Y(), 0)

go_back_1m: path = (
    initial,
    [],
    (initial[0] - 1, initial[1], 0),
)

go_forward_1m: path = (
    (initial[0] - 1, initial[1], 0),
    [],
    initial,
)