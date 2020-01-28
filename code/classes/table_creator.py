from code.classes.grid import Grid
from code.classes.connection import Connection

import csv

def table_creator(grid):
    connections = grid.connections_list
    with open ('results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Gate A", "Gate B" , "Wire coordinates"])
        for connection in connections:
            writer.writerow([1, 1, connection])
    
