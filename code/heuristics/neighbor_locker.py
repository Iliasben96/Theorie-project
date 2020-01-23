class NeighborLocker:

    def __init__(self, grid):

        self.all_neighbors = []
        self.gate_neighbor_coordinates = {}
        self.make_gate_neighbors(grid)

        self.closed_neighbors = {}


    def check_if_neighbor(self, position, grid):
        if position in self.gate_neighbor_coordinates:
            gate_numbers = self.gate_neighbor_coordinates[position]
            for gate_nr in gate_numbers:
                    gate = grid.gate_list[gate_nr - 1]
                    gate.used_neighbors += 1



    def make_gate_neighbors(self, grid):

        for gate in grid.gate_list:
            neighbors = grid.get_gate_neighbors(gate.coordinates)
            gate.neighbors = neighbors

            for neighbor in neighbors:
                if neighbor not in self.gate_neighbor_coordinates:
                    self.gate_neighbor_coordinates[neighbor] = [gate.nr]
                else:
                    gate_nr_list = self.gate_neighbor_coordinates[neighbor]
                    gate_nr_list.append(gate.nr)
                    self.gate_neighbor_coordinates[neighbor] = gate_nr_list

        print(self.gate_neighbor_coordinates)

    def lock_gate_neighbors(self, grid):

        while self.lock_if_all_neighbors_used(grid):

            for neighbor,owner in self.closed_neighbors.items():
                if neighbor in self.gate_neighbor_coordinates and neighbor not in self.all_neighbors:
                    self.all_neighbors.append(neighbor)
                    gate_numbers = self.gate_neighbor_coordinates[neighbor]
                    for gate_nr in gate_numbers:
                        if gate_nr != owner:
                            gate = grid.gate_list[gate_nr - 1]
                            gate.used_neighbors += 1

        return self.closed_neighbors


    def lock_if_all_neighbors_used(self, grid):

        locked = False
        for gate in grid.gate_list:
            if gate.get_available_connections() == 0:
                neighbors = gate.neighbors
                for neighbor in neighbors:
                    if neighbor not in self.closed_neighbors:
                        locked = True
                        self.closed_neighbors[neighbor] = gate.nr

        return locked

    """
    Add back neighbors as walkable terrain
    """
    def add_back_gate_neighbors(self, grid, start_gate, goal_gate):
        
        all_wires = grid.all_wires
        mother_grid = grid.mother_grid

        start_nr = start_gate.nr
        start_neighbors = []

        gate_is_locked = False
        for neighbor,gate_nr in self.closed_neighbors.items():
            if start_nr == gate_nr:
                gate_is_locked = True
                start_neighbors.append(neighbor)

        if gate_is_locked == False:
            start_neighbors = grid.get_gate_neighbors(start_gate.coordinates)

        found_wire = False

        # Loop over neighbors of start point
        for start_neighbor in start_neighbors:

            # Check if the neighbor has a wire in its place
            for wire in all_wires:
                
                if start_neighbor == wire:
                    found_wire == True
                    
            neighbor_already_placed = False
            
            # Only add back the neighbor as walkable terrain if it is not a wire
            if found_wire == False:
                base_grid = mother_grid[start_neighbor[2]]
                start_neighbor_correct_row = base_grid[start_neighbor[1]]
                for x in start_neighbor_correct_row:
                    
                    if x == start_neighbor[0]:
                        neighbor_already_placed = True
                if neighbor_already_placed == False:
                    start_neighbor_correct_row.append(start_neighbor[0])
                    mother_grid[start_neighbor[2]][start_neighbor[1]] = start_neighbor_correct_row


        goal_nr = goal_gate.nr
        goal_neighbors = []

        gate_is_locked = False
        for neighbor,gate_nr in self.closed_neighbors.items():
            if goal_nr == gate_nr:
                gate_is_locked = True
                goal_neighbors.append(neighbor)

        if gate_is_locked == False:
            goal_neighbors = grid.get_gate_neighbors(goal_gate.coordinates)

        found_wire = False

        for goal_neighbor in goal_neighbors:

            for wire in all_wires:

                if goal_neighbor == wire:
                    found_wire == True
            
            neighbor_already_placed = False
                    
            if found_wire == False:
                base_grid = mother_grid[goal_neighbor[2]]
                goal_neighbor_correct_row = base_grid[goal_neighbor[1]]
                for x in goal_neighbor_correct_row:                    
                    if x == goal_neighbor[0]:
                        neighbor_already_placed = True
                if neighbor_already_placed == False:
                    goal_neighbor_correct_row.append(goal_neighbor[0])
                    mother_grid[goal_neighbor[2]][goal_neighbor[1]] = goal_neighbor_correct_row

        return mother_grid

    """
    Relock the neighbors of the gate 
    """
    def relock_gate_neighbors(self, grid, start_gate, goal_gate):

        temp_grid = {} 
        all_wires = grid.all_wires
        mother_grid = grid.mother_grid


        start_nr = start_gate.nr
        start_neighbors = []

        gate_is_locked = False
        for neighbor,gate_nr in self.closed_neighbors.items():
            if start_nr == gate_nr:
                gate_is_locked = True
                start_neighbors.append(neighbor)

        if gate_is_locked == False:
            start_neighbors = grid.get_gate_neighbors(start_gate.position)


        # Lock neighbors to not be walkable anymore
        start_neighbors = grid.get_gate_neighbors(start_gate.coordinates)

        for start_neighbor in start_neighbors:
            temp_grid = mother_grid[start_neighbor[2]]
            start_neighbor_correct_row = temp_grid[start_neighbor[1]]

            if start_neighbor[0] in start_neighbor_correct_row:
                start_neighbor_correct_row.remove(start_neighbor[0])

        goal_neighbors = grid.get_gate_neighbors(goal_gate.coordinates)

        for goal_neighbor in goal_neighbors:
            temp_grid = mother_grid[goal_neighbor[2]]
            goal_neighbor_correct_row = temp_grid[goal_neighbor[1]]
            if goal_neighbor[0] in goal_neighbor_correct_row:
                goal_neighbor_correct_row.remove(goal_neighbor[0])

        return mother_grid