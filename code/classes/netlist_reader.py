import csv


def netlistreader(chip_number, netlist_number):
    """Function to load the provided csv netlist file"""
    
    netlist = []
    first_row = True

    # Construct filepath
    file_to_open = "data/gates&netlists/chip_" + str(chip_number) +  "/netlist_" + str(netlist_number) + ".csv"

    # Open this file
    with open(file_to_open, newline='') as gatesfile:
        filereader = csv.reader(gatesfile, delimiter=' ', quotechar = '|')
    
        # Loop over csv rows
        for row in filereader:
            # Skip first row
            if first_row:
                first_row = False
                continue
            
            # Remove comma and add to list
            for i in range(0, 2):
                row[i] = row[i].strip(',')
                row[i] = int(row[i])
            netlist.append(row)
    return netlist