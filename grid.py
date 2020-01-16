from gate import Gate
import csv
from netlist_reader import netlistreader
from connection import Connection

class Grid: 

    def __init__(self, chip_nr):
        self.chip_nr = chip_nr
        self.read_chip_csv(chip_nr)
        self.get_start_grid(chip_nr)

    # Global list that holds all 7 z levels of the x by y grids
    mother_grid = {}

    # Ordered list of all gates
    gate_list = []

    # List of all wires
    connections_list = []

    grid_max_x = 0
    grid_max_y = 0

    temporary_gate_list = []

    wire_count = 0

    # function to calculate how many gates a print list has
    def read_chip_csv(self, chip_nr):
        counter = 0

        first_row = True

        # Create path to open chip
        path = 'gates&netlists/chip_' + str(chip_nr) + '/print_' + str(chip_nr) + '.csv'

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

                Grid.temporary_gate_list.append(row)

        return counter          

    # Create the start grid according to a chip_nr with a set amount of gates
    def get_start_grid(self, chip_nr):

        # Lists to later figure out the maximum coordinates of a gate
        all_x = []
        all_y = []

        # Fill array with empty gates
        empty_gate = Gate(0, 0, 0)
        Grid.gate_list = [empty_gate] * self.read_chip_csv(chip_nr)

        for gate_data in Grid.temporary_gate_list:
            gate_nr = int(gate_data[0])
            gate_x = int(gate_data[1])
            gate_y = int(gate_data[2])

            # Add the coordinates of the gate to a list
            all_x.append(gate_x)
            all_y.append(gate_y)

            # Create new gate object and add it to the list of gates
            new_gate = Gate(gate_nr, gate_x, gate_y)
            Grid.gate_list[gate_nr - 1] = new_gate

        # Calculate max_x and max_y to create grids
        max_x = max(all_x)
        max_y = max(all_y)

        # Variables required to padding around the edges of the grid
        padding_x = 2
        padding_y = 2

        grid_max_x = max_x + padding_x
        grid_max_y = max_y + padding_y

        self.grid_max_y = grid_max_y

        Grid.grid_max_x = grid_max_x
        Grid.grid_max_y = grid_max_y

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

            Grid.mother_grid[z] = grid

        # Put gates in grid at z level 0
        for gate in Grid.gate_list:
            base_grid = Grid.mother_grid[0]
            correct_row = base_grid[gate.y]
            correct_row.remove(gate.x)

            # Remove neighbours
            

        return Grid.mother_grid

    # Function that prints out all layers of the grid to the console
    def print_grid(self, z):
        base_grid = Grid.mother_grid[z]
        for y, x in base_grid.items():
            print("Y = %d"% (y))
            print(x)

    # Function that returns all neighbors of a position
    def get_neighbors(self, position):

        x = position[0]
        y = position[1]
        z = position[2]

        neighbors = []
        mother_grid = Grid.mother_grid
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

    # Function to get coordinates of a certain gate number
    def get_gate_coordinate(self, gate_nr):

        gate = Grid.gate_list[gate_nr - 1]
        coordinates = {
            "x" : gate.x,
            "y" : gate.y
        }

        return coordinates

    # Function that adds a set of wires, called connection, to a list of connections
    def put_connection(self, connection):
        for wire in connection:

            base_grid = Grid.mother_grid[wire[2]]

            correct_row = base_grid[wire[1]]

            correct_row.remove(wire[0])

            # Count total length of all wires
            Grid.wire_count += 1

        Grid.connections_list.append(connection)

    # Add start and end gates as walkable terrain when they are being used
    def add_start_end_gates(self, start, end):
        start_x = start[0]
        start_y = start[1]
        base_grid_index = 0

        end_x = end[0]
        end_y = end[1]

        grid = Grid.mother_grid[base_grid_index]

        start_correct_row = grid[start_y]
        start_correct_row.append(start_x)

        end_correct_row = grid[end_y]
        end_correct_row.append(end_x)

        Grid.mother_grid[base_grid_index] = grid