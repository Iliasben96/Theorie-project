from netlist_reader import netlistreader
from grid import Grid
from gate import Gate
from plot import Plot
from algorithms import Algorithms
from priority_queue import PriorityQueue
from solving_loop import SolvingLoop
from test_solver import TestSolver

if __name__ == "__main__":

    netlist = netlistreader(1, 1)

    # Make new grid instance
    grid = Grid(1, netlist, True)

    sl = SolvingLoop(grid, netlist)

    sl.get_priority_center_grid()
    sl.solver()

    print("Wires not solved %d " % (sl.not_solved_counter))
    print("Wires solved %d" % (30 - sl.not_solved_counter))
    print("Wires used: %d" % (grid.wire_count))
    wires_per_connection = grid.wire_count / (30 - sl.not_solved_counter)
    print("Wires per succesfull connection")
    print(wires_per_connection)

    chip_plot = Plot(grid)
    chip_plot.plot()