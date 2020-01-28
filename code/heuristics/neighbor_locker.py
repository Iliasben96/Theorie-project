from code.heuristics.connection_amount import get_connections_per_gate

class NeighborLocker:

    """Class that can lock and relock neighbors. Mainly used to lock certain gates at every step of Astar"""

    def __init__(self, grid):
        self.grid = grid
        self.connections_per_gate = grid.connections_per_gate
        self.neighbor_gate_link = grid.neighbors_gates_link


    def get_available_neighbors_dict(self):
        """Make a list of gate numbers with the amount of connections after them"""
        available_neighbors_amounts = {}
        for gate,connection_amount in self.connections_per_gate.items():
            available_neighbors_amounts[gate] = 5 - connection_amount
        return available_neighbors_amounts

    def get_all_gate_neighbors(self):
        return self.neighbor_gate_link


    def lock_neighbors(self, available_neighbors_amounts, locked_neighbors, start_gate_nr, goal_gate_nr):
        """Loops over the available neighbors dict and returns what neighbors should be locked because of this"""

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

    def get_new_available_neighbors(self, position, all_gate_neighbors, locked_neighbors, available_neighbors):
        """Gets the available neighbors per gate, returns it as a dict with gate_nr as key and available neighbors as value"""

        # If the current is a neighbor of a gate, and not locked
        if position in all_gate_neighbors and position not in locked_neighbors:

            neighbors_to_check = all_gate_neighbors[position]

            # Loop over list of gates that have this neighbor
            for gate_nr in neighbors_to_check:

                # Check if the gate has an open spot in available gate neigbors
                if gate_nr in available_neighbors and available_neighbors[gate_nr] > 0:

                        # If it has an available spot, 
                        temp = available_neighbors[gate_nr]
                        temp -= 1
                        available_neighbors[gate_nr] = temp

        return available_neighbors

    def lock_double_neighbors(self, locked_neighbors, all_gate_neighbors, available_neighbors):
        """Function that looks if new locked situation should make sure other gates lock asswell"""

        for locked_neighbor in locked_neighbors:
            neighbors_to_check = all_gate_neighbors[locked_neighbor]

            for gate_nr in neighbors_to_check:
                if gate_nr in available_neighbors and available_neighbors[gate_nr] > 0:
                    temp = available_neighbors[gate_nr]
                    temp -= 1
                    available_neighbors[gate_nr] = temp

        return available_neighbors
