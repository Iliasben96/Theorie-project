from code.heuristics.manhattan import manhattan_heuristic

def get_connection_length_priority(gate_connections):

    # Calculate priority for each connection

        # TODO: sort the connection based on the lowest manhattan heuristic
    for connection_nr in gate_connections:
        connection = gate_connections[connection_nr]
        gate_a = connection.gate_a
        gate_b = connection.gate_b

        priority = manhattan_heuristic(gate_a.coordinates, gate_b.coordinates)

        connection.priority += priority

    return gate_connections