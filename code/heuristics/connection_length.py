from code.heuristics.manhattan import manhattan_heuristic

def get_connection_length_priority(gate_connections):

    # loops over all connections in the netlist
    for connection_nr in gate_connections:
        connection = gate_connections[connection_nr]
        gate_a = connection.gate_a
        gate_b = connection.gate_b

        # creates a priority based on the distance of the manhattan heuristic
        priority = manhattan_heuristic(gate_a.coordinates, gate_b.coordinates)
        connection.priority += priority

    return gate_connections