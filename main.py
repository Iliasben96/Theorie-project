from code.classes.netlist_reader import netlistreader
from code.classes.grid import Grid
from code.classes.gate import Gate
from code.visualisation.plot import Plot
from code.classes.solving_loop import SolvingLoop

if __name__ == "__main__":

    netlist = netlistreader(2,5)

    # # Make new grid instance
    grid = Grid(2, netlist, True)

    sl = SolvingLoop(grid, netlist)
    # connections_per_gate = sl.get_connections_per_gate()

    sl.start(3)

    print("Wires not solved %d " % (sl.not_solved_counter))
    print("Wires solved %d" % (30 - sl.not_solved_counter))
    print("Wires used: %d" % (grid.wire_count))
    wires_per_connection = grid.wire_count / (30 - sl.not_solved_counter)
    print("Wires per succesfull connection")
    print(wires_per_connection)

    chip_plot = Plot(grid)
    chip_plot.plot()