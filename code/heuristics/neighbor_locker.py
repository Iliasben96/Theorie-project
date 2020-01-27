from code.heuristics.connection_amount import get_connections_per_gate

class NeighborLocker:

    def __init__(self, grid):
        self.grid = grid
        self.connections_per_gate = grid.connections_per_gate
        self.neighbor_gate_link = grid.neighbors_gates_link

    # Make a list of gate numbers with the amount of connections after them
    def get_available_neighbors_dict(self):
        available_neighbors_amounts = {}
        for gate,connection_amount in self.connections_per_gate.items():
            available_neighbors_amounts[gate] = 5 - connection_amount
        return available_neighbors_amounts

    def get_all_gate_neighbors(self):
        return self.neighbor_gate_link

    # Loops over the available neighbors dict and returns what neighbors should be locked because of this
    def lock_neighbors(self, available_neighbors_amounts, locked_neighbors, start_gate_nr, goal_gate_nr):

        for gate_nr,available_neighbor_amount in available_neighbors_amounts.items():

            # Make sure not to include the goal and end, so their neighbors can be used
            if gate_nr != start_gate_nr and gate_nr != goal_gate_nr:

                # Only lock if a certain gate has no more free connections, provided how many connections they need and how many neighbors have been used up
                if available_neighbor_amount == 0:

                    # Seek the right gate from the gate list
                    gate = self.grid.gate_list[gate_nr - 1]

                    # Get the coordinates of this gate
                    neighbors_to_lock = self.grid.get_gate_neighbors(gate.coordinates)

                    # Loop over all the neighbors
                    for neighbor in neighbors_to_lock:

                        # If it hasn't been locked
                        if neighbor not in locked_neighbors:
                            # Lock it
                            locked_neighbors[neighbor] = gate_nr
        # Return all the neighbors that have been locked
        return locked_neighbors      