from code.classes.gate import Gate
from code.classes.connection import Connection
from code.heuristics.connection_amount import get_connections_per_gate

import csv
import random

class Grid: 
    """Class that holds a dictionary as grid and that handles all actions involving this grid
    For example removing and placing coordinates, retrieving neighbors of coordinates, etc.
    """

    def __init__(self, chip_nr, netlist, neighbor_lock_nr):
        self.chip_nr = chip_nr

        # Option to apply heuristic to remove neighbors
        self.neighbor_lock_nr = neighbor_lock_nr

        self.netlist = netlist

        # Variables that will hold the max x and max y of the grid, they are later initialised according to the chip_nr
        self.grid_max_x = 0
        self.grid_max_y = 0

        # Global list that holds all 7 Z levels of the x by y grids
        self.mother_grid = {}

        # Gate_list to hold gates temporarily, before they are moved into the gate_list
        self.temporary_gate_list = []

        # Ordered list of all gates
        self.gate_list = []

        # Dict of wired_connections
        self.wired_connections = {}

        # Dictionary of all connections as connection objects
        self.gate_connections = {}

        # List containing all coordinates used by wires
        self.all_wires = []

        # Counter to keep track of amount of wires used
        self.wire_count = 0

        # Dictionary that has the coordinates of a neighbor of a gate as key, and the gate numbers that have this neighbor as values
        self.neighbors_gates_link = {}

        # List with tuples containing the coordinates of all neighbors of all gates
        self.all_gate_neighbors = []

        # Get a dictionary with the amount of connections for each gate, according to the provided netlist
        self.connections_per_gate = get_connections_per_gate(self.netlist)

        # Get the amount of gates from the chip_csv file
        self.gate_count = self.read_chip_csv(chip_nr)

        # Init the start grid
        self.get_start_grid(chip_nr)

        # Generate a list with connection objects
        self.make_connections_dict()


    def read_chip_csv(self, chip_nr):
        """ Function to calculate how many gates a print list has"""

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

    def get_start_grid(self, chip_nr):
        """Create the start grid according to a chip_nr with a set amount of gates"""

        # Lists to later figure out the maximum coordinates of a gate
        all_x = []
        all_y = []

        # Fill array with empty gates
        empty_gate = Gate(0, (0, 0, 0), 0)
        self.gate_list = [empty_gate] * self.gate_count


        # Make the temporary gate list into the final gatelist
        for gate_data in self.temporary_gate_list:
            gate_nr = int(gate_data[0])
            gate_x = int(gate_data[1])
            gate_y = int(gate_data[2])
            gate_connection_amount = 0
            if gate_nr in self.connections_per_gate:
                gate_connection_amount = self.connections_per_gate[gate_nr]


            # Make tuple to store the coordinates of the gate, (x, y, z)
            gate_coordinates = (gate_x, gate_y, 0)

            # Add the coordinates of the gate to a list
            all_x.append(gate_x)
            all_y.append(gate_y)

            # Create new gate object and add it to the list of gates
            new_gate = Gate(gate_nr, gate_coordinates, gate_connection_amount)

            # TODO: make this a dict
            # Gatelist that stores all gates
            self.gate_list[gate_nr - 1] = new_gate

        # Calculate max_x and max_y to create grids
        max_x = max(all_x)
        max_y = max(all_y)

        # Variables required to padding around the edges of the grid
        padding_x = 2
        padding_y = 2

        # Give grid a max_x and max_y, taken into account the padding
        grid_max_x = max_x + padding_x
        grid_max_y = max_y + padding_y

        self.grid_max_x = grid_max_x
        self.grid_max_y = grid_max_y

        # Create Z amount of empty layers 
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

        # Init list to make sure that later, neighbors of unconnected gates are not locked
        connected_gates = []

        # Loop over all connections in gate list
        for gate in self.gate_list:
            # Check if the gate is in the netlist
            for connection in self.netlist:
                if gate.nr in connection and gate.nr not in connected_gates:

                    # If it is, add the nummber to a new list
                    connected_gates.append(gate.nr)

            # Remove coordinates of gates from grid, so that Astar can't use it to make a path later
            gate_coordinates = gate.coordinates
            self.remove_coordinate(gate_coordinates)
        self.get_all_gate_neighbor_dict(connected_gates)

        """If neighbor lock option is 2, meaning gates should be locked at the init, 
        remove the coordinates of the neighbors from the grid"""
        if self.neighbor_lock_nr == 2:
            self.remove_gate_neighbors()

        return self.mother_grid

    def place_coordinate(self, coordinates):
        """
        Places a coordinate in the grid
        """

        # Get the correct row from the mother_grid
        row_to_place = self.mother_grid[coordinates[2]][coordinates[1]]
        
        # Only place if the coordinate does not yet exist
        if coordinates[0] not in row_to_place:
            row_to_place.append(coordinates[0])
            return True
        return False

    def remove_coordinate(self, coordinates):
        """
        Removes a coordinate from the grid
        """

        # Get correct row from the mother grid
        row_to_remove = self.mother_grid[coordinates[2]][coordinates[1]]

        # Only remove the coordinate if it exists
        if coordinates[0] in row_to_remove:
            row_to_remove.remove(coordinates[0])
            return True
        return False


    def get_all_gate_neighbor_dict(self, connected_gates):
        """Returns all neighbors of all connected gates
        """

        # For each gate that has a connection according to the netlist
        for gate_nr in connected_gates:

            # Get gate_from gatelist
            gate = self.gate_list[gate_nr - 1]

            # Get neighbors of this gate
            neighbors = self.get_gate_neighbors(gate.coordinates)

            # Loop over the all neighbors
            for neighbor in neighbors:

                if neighbor not in self.neighbors_gates_link:

                    # Store gate number in dict, with coordinate of the gate as key
                    self.neighbors_gates_link[neighbor] = [gate_nr]
                else:

                    # If the neighbor is already in dict with gate_nr, add current gate_nr to list
                    self.neighbors_gates_link[neighbor].append(gate_nr)

                # Add neighbor to all_gate_neighbors, without duplicates
                if neighbor not in self.all_gate_neighbors:
                    self.all_gate_neighbors.append(neighbor)

    def remove_gate_neighbors(self):

        """
        Removes neighbors of every gate from the grid
        """
        for gate_neighbor in self.all_gate_neighbors:

            self.remove_coordinate(gate_neighbor)

    def make_connections_dict(self):
        """
        Makes all connections in netlist into connection objects and stores them in a dictionary
        """

        id_counter = 0
        for connection in self.netlist:

            # Get gate numbers from netlist
            gate_a_nr = connection[0]
            gate_b_nr = connection[1]

            # Get corresponding gates from gate_list
            start_gate = self.gate_list[gate_a_nr - 1]
            goal_gate = self.gate_list[gate_b_nr - 1]

            new_connection = Connection(start_gate, goal_gate, id_counter)

            # Add new Connection, with id as key and Connection object as value
            self.gate_connections[id_counter] = new_connection
            id_counter += 1


    def put_connection(self, path, connection):
        """
        Function takes a connection or path (usually from Astar) and removes the coordinates of each step from grid
        """

        # Loop over each coordinate in the path
        for coordinate in path:

            self.remove_coordinate(coordinate)

            # Count total length of all wires
            self.wire_count += 1

        # Make new connection dict with connection and path 
        connection_dict = {"path" : path, "connection" : connection}

        # Add connection_dict to dict with connections, indexed on it's ID
        self.wired_connections[connection.connection_id] = connection_dict


    def get_neighbors(self, position):
        """ 
        Function that returns all neighbor coordinates of a position
        """

        # Get coordinates from inputted tuple position
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


    def get_gate_neighbors(self, position):
        """
        Get neighbor coordinates of a gate
        """
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

    def add_start_end_gates(self, start, goal):
        """
        Add start and end gates as walkable terrain when they are being used
        """
        self.place_coordinate(start)
        self.place_coordinate(goal)


    def add_back_gate_neighbors(self, start, goal):
        """
        Add back neighbors as walkable terrain
        """
        start_neighbors = self.get_gate_neighbors(start)

        found_wire = False

        # Loop over neighbors of start point
        for start_neighbor in start_neighbors:

            # Check if the neighbor has a wire in its place
            for wire in self.all_wires:
                
                if start_neighbor == wire:
                    found_wire == True
    
            
            # Only add back the neighbor as walkable terrain if it is not a wire
            if found_wire == False:
                self.place_coordinate(start_neighbor)

        goal_neighbors = self.get_gate_neighbors(goal)

        found_wire = False

        for goal_neighbor in goal_neighbors:

            for wire in self.all_wires:

                if goal_neighbor == wire:
                    found_wire == True
                                
            if found_wire == False:
                self.place_coordinate(goal_neighbor)

    def relock_gate_neighbors(self, start, goal):
        """
        Relock the neighbors of the gate 
        """

        # Lock neighbors to not be walkable anymore
        start_neighbors = self.get_gate_neighbors(start)

        for start_neighbor in start_neighbors:
            self.remove_coordinate(start_neighbor)

        goal_neighbors = self.get_gate_neighbors(goal)

        for goal_neighbor in goal_neighbors:
            self.remove_coordinate(goal_neighbor)