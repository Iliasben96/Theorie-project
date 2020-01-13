from gate import Gate
import csv
from netlist_reader import netlistreader
from connection import Connection
from wire import Wire

class Grid: 

    # Global list that holds all 7 z levels of the x by y grids
    mother_grid = []

    # Ordered list of all gates
    gate_list = []

    # List of all wires
    wire_list = []

    grid_max_x = 0
    grid_max_y = 0

    # Create the start grid according to a chip_nr with a set amount of gates
    def get_start_grid(self, chip_nr, gate_amount):
  
        # List that holds all layers 
        # TODO: rename this
        mother_grid = []

        # Set first row to True, used to skip first line
        first_row = True

        # Lists to later figure out the maximum coordinates of a gate
        all_x = []
        all_y = []

        # Fill array with empty gates
        empty_gate = Gate(0, 0, 0)
        Grid.gate_list = [empty_gate] * gate_amount
        
        # Create path to open chip
        path = 'gates&netlists/chip_' + str(chip_nr) + '/print_' + str(chip_nr) + '.csv'

        # open CSV file
        with open(path, newline='') as gatesfile:
            filereader = csv.reader(gatesfile, delimiter=' ', quotechar = '|')

            # Loop over csv rows
            for row in filereader:

                # Skip first row
                if first_row:
                    first_row = False
                    continue

                # Remove comma
                for i in range(0, 2):
                    row[i] = row[i].strip(',')

                # Assign variables to gate objects from csv file
                gate_nr = int(row[0])
                gate_x = int(row[1])
                gate_y = int(row[2])

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
        padding_x = 1
        padding_y = 2

        grid_max_x = max_x + padding_x
        grid_max_y = max_y + padding_y

        Grid.grid_max_x = grid_max_x
        Grid.grid_max_y = grid_max_y

        # Create empty layers on top of base layer
        for z in range(0, 7):
            grid = []

            # Create fully empty grid with max values from gates
            for column in range(0, grid_max_y):
                row = []
                for item in range(0, grid_max_x):
                    row.append(0)
                
                # Add extra padding after each row 
                row.append(0)

                # Add each row to the grid
                grid.append(row) 
            mother_grid.append(grid)

        # Put gates in grid at z level 0
        for gate in Grid.gate_list:
            base_grid = mother_grid[0]
            correct_row = base_grid[gate.y]
            correct_row[gate.x] = 1
 
        # Modify global mother grid
        Grid.mother_grid = mother_grid

        return mother_grid

    # Function that prints out all layers of the grid to the console
    def print_grid(self):
        mother_grid = Grid.mother_grid
        counter = 0
        for grid in mother_grid:
            print("This is grid number: %d" % (counter))
            for row in grid:
                print(row)
            counter += 1
    
    # Function to get coordinates of a certain gate number
    def get_gate_coordinate(self, gate_nr):

        gate = Grid.gate_list[gate_nr - 1]
        coordinates = {
            "x" : gate.x,
            "y" : gate.y
        }

        return coordinates

    # Function that puts a 'wire' at an location in the grid based on x, y and z coordinates
    def put_wire(self, wire):
        
        mother_grid = Grid.mother_grid

        correct_grid = mother_grid[wire.z]

        correct_row = correct_grid[wire.y]

        Grid.wire_list.append(wire)

        correct_row[wire.x] = 2

        return
    
    def remove_start_end(self, start, end):
        grid = Grid.mother_grid[0]

        start_correct_row = grid[start[1]]
        start_correct_row[start[0]] = 0

        end_correct_row = grid[end[1]]
        end_correct_row[end[0]] = 0

        Grid.mother_grid[0] = grid