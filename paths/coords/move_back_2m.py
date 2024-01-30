from units.SI import meters, radians
import constants
import math

coord = (meters, meters, radians)
waypoints = [(meters, meters)]
path = (coord, waypoints, coord)

blue_team = False

initial: coord = (0, 0, 0)

go_back_1m: path = (
    initial,
    [],
    (constants.ApriltagPositionDictRed[4].X() - 0.7, constants.ApriltagPositionDictRed[4].Y(), 0),
)

go_forward_1m: path = (
    (initial[0] - 1, initial[1] + 1, math.pi / -2),
    [],
    (initial[0], initial[1], 0),
)