from netlist_reader import netlistreader
from grid import Grid

print(netlistreader(1, 1))

start_grid = Grid()

grid = start_grid.get_start_grid(1, 25)
