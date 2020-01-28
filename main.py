from code.classes.netlist_reader import netlistreader
from code.classes.grid import Grid
from code.classes.gate import Gate
from code.visualisation.plot import Plot
from code.classes.chip_solver import ChipSolver
from code.algorithms.random_loop import start_random_solutions
from code.classes.table_creator import table_creator
from code.user_interface.user_interface import get_user_chip_nr, get_user_netlist_nr, get_user_heuristic_nr, get_user_neighbor_lock_nr

if __name__ == "__main__":
    
    # Get user inputs
    chip_nr = get_user_chip_nr()
    netlist_nr = get_user_netlist_nr(chip_nr)
    heuristic_nr = get_user_heuristic_nr()
    neighbor_lock_nr = get_user_neighbor_lock_nr()


    netlist = netlistreader(chip_nr,netlist_nr)

    # Make new grid instance
    grid = Grid(chip_nr, netlist, neighbor_lock_nr)

    chip_solver = ChipSolver(grid, netlist)
    chip_solver.start(heuristic_nr, neighbor_lock_nr)
    total_connections = len(netlist)

    table_creator(grid, netlist)

    # solution information
    print("Wires not solved %d " % (chip_solver.not_solved_counter))
    print("Wires solved %d" % (total_connections - chip_solver.not_solved_counter))
    print("Wires used: %d" % (grid.wire_count))
    wires_per_connection = grid.wire_count / (total_connections - chip_solver.not_solved_counter)
    print("Wires per succesfull connection")
    print(wires_per_connection)

    # generates visual plot
    chip_plot = Plot(grid)
    chip_plot.plot()