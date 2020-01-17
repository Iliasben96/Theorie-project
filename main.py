from netlist_reader import netlistreader
from grid import Grid
from gate import Gate
from plot import Plot
from algorithms import Algorithms
from priority_queue import PriorityQueue
from solving_loop import SolvingLoop

if __name__ == "__main__":

    netlist = netlistreader(1, 1)

    # Make new grid instance
    grid = Grid(1, netlist)

    sl = SolvingLoop(grid, netlist)

<<<<<<< HEAD
    sl.start(1)
=======
    sl.start(6)
>>>>>>> 7018536344faf045072bfcdc657212e71e849577

    print("Wires not solved %d " % (sl.not_solved_counter))
    print("Wires solved %d" % (31 - sl.not_solved_counter))
    print("Wires used: %d" % (grid.wire_count))
    wires_per_connection = grid.wire_count / (30 - sl.not_solved_counter)
    print("Wires per succesfull connection")
    print(wires_per_connection)

<<<<<<< HEAD
    # grid.add_back_gate_neighbors((1,1,0), (8,8,0))
    # grid.relock_gate_neighbors((1, 1, 0), (8, 8, 0))

    # Create new plot
    chip_plot = Plot(grid)
=======
    # # Create new plot
    # chip_plot = Plot(grid)
>>>>>>> 7018536344faf045072bfcdc657212e71e849577
    
    # # Show new plot
    # chip_plot.plot()