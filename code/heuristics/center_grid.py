from code.classes.grid import Grid
from code.heuristics.manhattan import manhattan_heuristic

def get_priority_center_grid(grid, gate_connections):
    """Gets priority depending on how close the gates in a connection are to the centre """

    # calculates grid center
    centre_x = abs(grid.grid_max_x / 2)
    centre_y = abs(grid.grid_max_y / 2)
    centre = (centre_x, centre_y, 0)


    for connection_nr in gate_connections:

        # gets the gates for the connection
        connection = gate_connections[connection_nr]
        gate_a = connection.gate_a
        gate_b = connection.gate_b

        # calculates the distance for each gate from the center
        gate_a_priority = manhattan_heuristic(gate_a.coordinates, centre)
        gate_b_priority = manhattan_heuristic(gate_b.coordinates, centre)

        # gives priority based on the total distance from the center
        priority = (gate_a_priority + gate_b_priority) / 2
        connection.priority = priority
        
    return gate_connections