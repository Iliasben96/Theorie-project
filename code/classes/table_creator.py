from code.classes.grid import Grid
from code.classes.connection import Connection

import csv

def table_creator(grid, netlist):
    with open ('results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Gate A", "Gate B" , "Wire coordinates"])

        id_counter = 0

        for net in netlist:
            if id_counter in grid.wired_connections:
                connection_dict = grid.wired_connections[id_counter]
                path = connection_dict["path"]
                connection_object = connection_dict["connection"]
                gate_a = connection_object.gate_a
                gate_b = connection_object.gate_b
                writer.writerow([gate_a.nr, gate_b.nr, path])
            else:
                writer.writerow([net[0], net[1], "No path found"])
            id_counter += 1

        
