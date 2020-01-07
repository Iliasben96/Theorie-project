# main programme that creates an optimal netlist between inputted gates on a grid

import csv 
from gate import Gate

# Array of gates
gate_list = []

# Create a grid to store the playing field
grid = []

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
        gate_list.append(new_gate)

# Calculate max_x
max_x = max(all_x)

# print("DEBUG: Max x = %s" % (max_x))

# Calculate max_y
max_y = max(all_y)
# print("DEBUG: Max y = %s" % (max_y))

# Variables required to padding around the edges of the grid
padding_x = 1
padding_y = 2


# Create fully empty grid with max values from gates
for column in range(0, max_y + padding_y):
    row = []
    for item in range(0, max_x + padding_x):
        row.append(0)
    
    # Add extra padding after each row 
    row.append(0)

    # Add each row to the grid
    grid.append(row) 

# DEBUG: print all gate numbers
for gate in gate_list:
    correct_row = grid[gate.y]
    correct_row[gate.x] = "GATE"

# DEBUG: print the rows of the grid
for row in grid:
    print(row)