from netlist_reader import netlistreader
from grid import Grid
from gate import Gate
from plot import Plot
from algorithms import Algorithms
from priority_queue import PriorityQueue
from solving_loop import SolvingLoop

if __name__ == "__main__":

    # Make new grid instance
    grid = Grid(1)

    netlist = netlistreader(1, 1)

    sl = SolvingLoop(grid, netlist)

    sl.start(3)

    print("Wires used: %d" % (grid.wire_count))

    # Create new plot
    chip_plot = Plot(grid)
    
    # Show new plot
    chip_plot.plot()