def manhattan_heuristic(current, goal):
    
    distance_x = abs(current[0]- goal[0])
    distance_y = abs(current[1] - goal[1])
    distance_z = abs(current[2] - goal[2])

    # TODO: Change this to make distance_z is actually a fair representation of the z distance
    # TODO: Only if z_current - z_goal != 0, distance_z is absolute, if it is not, it is the distance * 2
    h = distance_x + distance_y + (distance_z * 2)

    return h
    