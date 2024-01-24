from units.SI import meters, radians
import math

coord = (meters, meters, radians)
waypoints = [(meters, meters)]
path = (coord, waypoints, coord)

blue_team = False

initial: coord = (5, 5, 0)

go_back_2m: path = (
    initial,
    [],
    (initial[0] + 2, initial[1] + 2, math.pi / 2),
)