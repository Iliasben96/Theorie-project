from netlist_reader import netlistreader
from grid import Grid
from gate import Gate
from plot import Plot
from node import Node

if __name__ == "__main__":

    # Make new grid instance
    start_grid = Grid()

    # Generate start grid
    # TODO: Make this dynamic according to size of print
    grid = start_grid.get_start_grid(1, 25)

    # # Create new plot
    # chip_plot = Plot(start_grid)
    
    # # Show new plot
    # chip_plot.plot()

    test_node = Node()

    start = (1, 1, 1)
    goal = (8, 8, 1)

    test_node.astar(start_grid, start, goal)

    # DEBUG: print grid
    start_grid.print_grid(1)

    # start_grid.put_wire((1, 1, 5))