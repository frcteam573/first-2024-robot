from units.SI import meters, radians

coord = (meters, meters, radians)
waypoints = [(meters, meters)]
path = (coord, waypoints, coord)

blue_team = False

initial: coord = (5, 5, 0)

go_back_2m: path = (
    initial,
    [],
    (initial[0] + 2, initial[1], 0),
)