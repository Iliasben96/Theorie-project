def manhattan_heuristic(current, goal):
    """Calculates the manhatten distane between two coordinates"""

    distance_x = abs(current[0]- goal[0])
    distance_y = abs(current[1] - goal[1])
    distance_z = abs(current[2] - goal[2])

    h = distance_x + distance_y + (distance_z * 2)

    return h
    