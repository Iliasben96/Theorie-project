from code.classes.grid import Grid
from code.classes.connection import Connection

import csv

def table_creator(grid):
    with open ('results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Gate A", "Gate B" , "Wire coordinates"])
        for connection_dict in grid.wired_connections.values():
            path = connection_dict["path"]
            connection_object = connection_dict["connection"]
            gate_a = connection_object.gate_a
            gate_b = connection_object.gate_b
            writer.writerow([gate_a.nr, gate_b.nr, path])
    
