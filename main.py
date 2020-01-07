# main programme that creates an optimal netlist between inputted gates on a grid

import csv 
from gate import Gate

# Array of gates
gate_list = []

# Counter for csv file
first_row = True

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
        gate_nr = row[0]
        gate_x = row[1]
        gate_y = row[2]

        # Create new gate object and add it to the list of gates
        new_gate = Gate(gate_nr, gate_x, gate_y)
        gate_list.append(new_gate)

# DEBUG: print all gate numbers
for gate in gate_list:
    print(gate.nr)