from code.classes.gate import Gate
from code.classes.connection import Connection
import csv
import random

class Grid: 
    counter = 0

    def __init__(self, chip_nr, netlist, remove_neighbors):
        self.chip_nr = chip_nr

        # Option to apply heuristic to remove neighbors from grid when they're not used
        # Accepts True or False statement
        self.remove_neighbors = remove_neighbors

        self.netlist = netlist

        # Global list that holds all 7 z levels of the x by y grids
        self.mother_grid = {}

        # Ordered list of all gates
        self.gate_list = []

        # List of connections made by the algorithm
        self.connections_list = []

        self.gate_connections = {}

        # List with all coordinates used by wires
        self.all_wires = []

        self.grid_max_x = 0
        self.grid_max_y = 0

        self.temporary_gate_list = []

        self.gate_count = self.read_chip_csv(chip_nr)

        self.get_start_grid(chip_nr)

        self.make_connections()

        self.wire_count = 0

        Grid.counter += 1

    """
    function to calculate how many gates a print list has
    """
    def read_chip_csv(self, chip_nr):
        counter = 0

        first_row = True

        # Create path to open chip
        path = 'data/gates&netlists/chip_' + str(chip_nr) + '/print_' + str(chip_nr) + '.csv'

        # open CSV file
        with open(path, newline='') as gatesfile:
            filereader = csv.reader(gatesfile, delimiter=' ', quotechar = '|')
            # Loop over csv rows
            for row in filereader:

                if first_row:
                    first_row = False
                    continue
                counter += 1

                # Remove comma
                for i in range(0, 2):
                    row[i] = row[i].strip(',')

                self.temporary_gate_list.append(row)

        return counter          

    """
    Create the start grid according to a chip_nr with a set amount of gates
    """
    def get_start_grid(self, chip_nr):

        # Lists to later figure out the maximum coordinates of a gate
        all_x = []
        all_y = []

        # Fill array with empty gates
        empty_gate = Gate(0, (0, 0, 0))
        self.gate_list = [empty_gate] * self.gate_count

        for gate_data in self.temporary_gate_list:
            gate_nr = int(gate_data[0])
            gate_x = int(gate_data[1])
            gate_y = int(gate_data[2])

            gate_coordinates = (gate_x, gate_y, 0)

            # Add the coordinates of the gate to a list
            all_x.append(gate_x)
            all_y.append(gate_y)

            # Create new gate object and add it to the list of gates
            new_gate = Gate(gate_nr, gate_coordinates)
            self.gate_list[gate_nr - 1] = new_gate

        # Calculate max_x and max_y to create grids
        max_x = max(all_x)
        max_y = max(all_y)

        # Variables required to padding around the edges of the grid
        padding_x = 2
        padding_y = 2

        grid_max_x = max_x + padding_x
        grid_max_y = max_y + padding_y

        self.grid_max_y = grid_max_y

        self.grid_max_x = grid_max_x
        self.grid_max_y = grid_max_y

        # Create empty layers on top of base layer
        for z in range(0, 7):
            grid = {}

            # Create fully empty grid with max values from gates
            for y in range(0, grid_max_y):
                row = []
                for x in range(0, grid_max_x):
                    row.append(x)

                # Add each row to the grid
                grid[y] = row

            self.mother_grid[z] = grid

        connected_gates = []

        # Loop over all connections in gate list
        for gate in self.gate_list:

            # Check if the gate is in the netlist
            for connection in self.netlist:
                if gate.nr in connection and gate.nr not in connected_gates:

                    # If it is, add the nummber to a new list
                    connected_gates.append(gate.nr)

            # Remove coordinates of gates from grid
            gate_coordinates = gate.coordinates
            base_grid = self.mother_grid[gate_coordinates[2]]
            correct_row = base_grid[gate_coordinates[1]]
            correct_row.remove(gate_coordinates[0])

        if self.remove_neighbors == True:
            self.remove_gate_neighbors(connected_gates)

        return self.mother_grid

    """
    Removes neighbors of every gate from the grid
    """
    def remove_gate_neighbors(self, connected_gates):

        all_gate_neighbors = []

        connected_gates = []

        if self.remove_neighbors == True:
            # For each gate that has a connection according to the netlist
            for gate_nr in connected_gates:

                gate = self.gate_list[gate_nr - 1]
                # Get neighbors of this gate
                neighbors = self.get_neighbors(gate.coordinates)

                for neighbor in neighbors:

                    if neighbor not in all_gate_neighbors:

                        all_gate_neighbors.append(neighbor)

            # Remove all neighbors from grid
            for gate_neighbor in all_gate_neighbors:

                base_grid = self.mother_grid[gate_neighbor[2]]
                correct_row = base_grid[gate_neighbor[1]]
                
                for x in correct_row:
                    if gate_neighbor[0] == x:
                        correct_row.remove(gate_neighbor[0])


    def make_connections(self):
        id_counter = 0
        for connection in self.netlist:

            # Get gate numbers from netlist
            gate_a_nr = connection[0]
            gate_b_nr = connection[1]

            # Get corresponding gates from gate_list
            start_gate = self.gate_list[gate_a_nr - 1]
            goal_gate = self.gate_list[gate_b_nr - 1]

            new_connection = Connection(start_gate, goal_gate, id_counter)
            self.gate_connections[id_counter] = new_connection
            id_counter += 1

    """ 
    Function that returns all neighbors of a position
    """
    def get_neighbors(self, position):

        x = position[0]
        y = position[1]
        z = position[2]

        neighbors = []
        mother_grid = self.mother_grid
        grid = mother_grid[z]

        # All possible moving positions
        x_left = x - 1
        x_right = x + 1
        y_up = y + 1
        y_down = y - 1
        z_level_up = z + 1
        z_level_down = z - 1

        # Check if neigbors are legal, add legal ones to list of neighbors
        if (y_up in grid and x in grid[y_up]):
            up_neighbor = (x, y_up, z)
            neighbors.append(up_neighbor)
        if (y_down in grid and x in grid[y_down]):
            down_neighbor = (x, y_down, z)
            neighbors.append(down_neighbor)
        if (x_left in grid[y]):
            left_neighbor = (x_left, y, z)
            neighbors.append(left_neighbor)
        if (x_right in grid[y]):
            right_neighbor = (x_right, y, z)
            neighbors.append(right_neighbor)
        if (z_level_up in mother_grid and x in mother_grid[z_level_up][y]):
            level_up_neighbor = (x, y, z_level_up)
            neighbors.append(level_up_neighbor)
        if (z_level_down in mother_grid and x in mother_grid[z_level_down][y]):
            level_down_neighbor = (x, y, z_level_down)
            neighbors.append(level_down_neighbor)

        return(neighbors)

    """
    Get neighbors of all gates
    """
    def get_gate_neighbors(self, position):
        x = position[0]
        y = position[1]
        z = position[2]

        neighbors = []

        # All possible moving positions
        x_left = x - 1
        x_right = x + 1
        y_up = y + 1
        y_down = y - 1
        z_level_up = z + 1

        # Check if neigbors are legal, add legal ones to list of neighbors

        up_neighbor = (x, y_up, z)
        if up_neighbor not in self.all_wires: 
            neighbors.append(up_neighbor)

        down_neighbor = (x, y_down, z)
        if down_neighbor not in self.all_wires:
            neighbors.append(down_neighbor)

        left_neighbor = (x_left, y, z)
        if left_neighbor not in self.all_wires:
            neighbors.append(left_neighbor)

        right_neighbor = (x_right, y, z)
        if right_neighbor not in self.all_wires:
            neighbors.append(right_neighbor)

        level_up_neighbor = (x, y, z_level_up)
        if level_up_neighbor not in self.all_wires:
            neighbors.append(level_up_neighbor)

        return(neighbors)

    """
    Function that adds a set of wires, called connection, to a list of connections
    """
    def put_connection(self, connection):
        for wire in connection:

            base_grid = self.mother_grid[wire[2]]

            correct_row = base_grid[wire[1]]

            correct_row.remove(wire[0])

            # Count total length of all wires
            self.wire_count += 1

        self.connections_list.append(connection)

    """
    Add start and end gates as walkable terrain when they are being used
    """
    def add_start_end_gates(self, start, goal):
        start_x = start[0]
        start_y = start[1]
        base_grid_index = 0

        goal_x = goal[0]
        goal_y = goal[1]

        grid = self.mother_grid[base_grid_index]

        start_correct_row = grid[start_y]
        start_correct_row.append(start_x)

        end_correct_row = grid[goal_y]
        end_correct_row.append(goal_x)

        self.mother_grid[base_grid_index] = grid

    """
    Add back neighbors as walkable terrain
    """
    def add_back_gate_neighbors(self, start, goal):
        start_neighbors = self.get_gate_neighbors(start)

        found_wire = False

        # Loop over neighbors of start point
        for start_neighbor in start_neighbors:

            # Check if the neighbor has a wire in its place
            for wire in self.all_wires:
                
                if start_neighbor == wire:
                    found_wire == True
                    
            neighbor_already_placed = False
            
            # Only add back the neighbor as walkable terrain if it is not a wire
            if found_wire == False:
                base_grid = self.mother_grid[start_neighbor[2]]
                start_neighbor_correct_row = base_grid[start_neighbor[1]]
                for x in start_neighbor_correct_row:
                    
                    if x == start_neighbor[0]:
                        neighbor_already_placed = True
                if neighbor_already_placed == False:
                    start_neighbor_correct_row.append(start_neighbor[0])
                    self.mother_grid[start_neighbor[2]][start_neighbor[1]] = start_neighbor_correct_row

        goal_neighbors = self.get_gate_neighbors(goal)

        found_wire = False

        for goal_neighbor in goal_neighbors:

            for wire in self.all_wires:

                if goal_neighbor == wire:
                    found_wire == True
            
            neighbor_already_placed = False
                    
            if found_wire == False:
                base_grid = self.mother_grid[goal_neighbor[2]]
                goal_neighbor_correct_row = base_grid[goal_neighbor[1]]
                for x in goal_neighbor_correct_row:                    
                    if x == goal_neighbor[0]:
                        neighbor_already_placed = True
                if neighbor_already_placed == False:
                    # print("Neighbor not yet placed")
                    goal_neighbor_correct_row.append(goal_neighbor[0])
                    self.mother_grid[goal_neighbor[2]][goal_neighbor[1]] = goal_neighbor_correct_row

    """
    Relock the neighbors of the gate 
    """
    def relock_gate_neighbors(self, start, goal):

        grid = {} 

        # Lock neighbors to not be walkable anymore
        start_neighbors = self.get_gate_neighbors(start)

        for start_neighbor in start_neighbors:
            grid = self.mother_grid[start_neighbor[2]]
            start_neighbor_correct_row = grid[start_neighbor[1]]

            if start_neighbor[0] in start_neighbor_correct_row:
                start_neighbor_correct_row.remove(start_neighbor[0])

        goal_neighbors = self.get_gate_neighbors(goal)

        for goal_neighbor in goal_neighbors:
            grid = self.mother_grid[goal_neighbor[2]]
            goal_neighbor_correct_row = grid[goal_neighbor[1]]
            if goal_neighbor[0] in goal_neighbor_correct_row:
                goal_neighbor_correct_row.remove(goal_neighbor[0])

    def increase_level(self):
        # Select correct wires
        for connection in self.connections_list:
            if len(connection) > 4:
                second_wire = connection[1]
                second_last_wire = connection[-2]

                # Create new wire with added Z coördinate
                insert_third_wire_list = list(second_wire)
                insert_third_wire_list[2] += 1
                insert_third_wire = tuple(insert_third_wire_list)

                # Create new wire with added Z coördinate
                insert_third_last_wire_list = list(second_last_wire)
                insert_third_last_wire_list[2] += 1
                insert_third_last_wire = tuple(insert_third_last_wire_list)

                # Insert third and third to last wire
                connection.insert(2, insert_third_wire)
                connection.insert(-2, insert_third_last_wire)

        # Increase Z coördinate of every cable between third and third to last wire
        for connection in self.connections_list:
            if len(connection) > 4:
                counter = 0
                max_wires = len(connection)
                for wire in connection:
                    if (max_wires - 3) > counter and counter > 2:
                        list_wire = list(wire)
                        list_wire[2] += 1
                        insert_wire = tuple(list_wire)
                    else:
                        insert_wire = wire
                    connection[counter] = insert_wire
                    counter += 1
            print(connection)