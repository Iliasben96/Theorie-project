# main programme that creates an optimal netlist between inputted gates on a grid
from gate import Gate
import csv
from netlist_reader import netlistreader

# Array of gates

max_n_chips = 26

# TODO: make this dynamic
empty_gate = Gate(0, 0, 0)
gate_list = [empty_gate] * max_n_chips

# Create a grid to store the playing field
mother_grid = []

# Counter for csv file
first_row = True

# Lists to later figure out the maximum coordinates of a gate
all_x = []
all_y = []

# open CSV file
with open('gates&netlists/chip_1/print_1.csv', newline='') as gatesfile:
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

        # Assign variables from csv file
        gate_nr = int(row[0])
        gate_x = int(row[1])
        gate_y = int(row[2])

        # Add the coordinates of the gate to a list
        all_x.append(gate_x)
        all_y.append(gate_y)

        # Create new gate object and add it to the list of gates
        new_gate = Gate(gate_nr, gate_x, gate_y)
        gate_list[gate_nr] = new_gate

print(netlistreader(1, 1))


# Calculate max_x
max_x = max(all_x)

# print("DEBUG: Max x = %s" % (max_x))

# Calculate max_y
max_y = max(all_y)
# print("DEBUG: Max y = %s" % (max_y))

# Variables required to padding around the edges of the grid
padding_x = 1
padding_y = 2

# Create empty layers on top of base layer
for z in range(7):
    grid = []

    # Create fully empty grid with max values from gates
    for column in range(0, max_y + padding_y):
        row = []
        for item in range(0, max_x + padding_x):
            row.append(0)
        
        # Add extra padding after each row 
        row.append(0)

        # Add each row to the grid
        grid.append(row) 
    mother_grid.append(grid)


# DEBUG: print all gate numbers
for gate in gate_list:

    base_grid = mother_grid[0]
    correct_row = base_grid[gate.y]
    correct_row[gate.x] = "GATE"

counter = 0
# DEBUG: print the rows of the grid
for grid in mother_grid:
    print("This is grid number: %d" % (counter))
    for row in grid:
        print(row)
    counter += 1