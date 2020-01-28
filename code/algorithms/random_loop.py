from code.classes.grid import Grid
from code.visualisation.plot import Plot
from code.heuristics.random_priority import get_random_priority


def start_random_solutions(grid, iterations, chip_solver):
    """ A loop to run the random algorithm over the netlist
    After generating a random order of the netlist the paths are put and the algorithm checks if solutions are found. 
    This process repeats until the maximun iterations is reached or a solution is found.
    """

    chip_nr = grid.chip_nr
    netlist = grid.netlist
    neighbor_lock_nr = grid.neighbor_lock_nr

    # loops for the amount of iterations the user specified
    for i in range(iterations):
        
        # Make new grid instance
        grid = Grid(chip_nr, netlist, neighbor_lock_nr)
        # runs the alogrithm for a random order of the netlist
        random_gate_connections = get_random_priority(chip_solver.gate_connections)
        sorted_random_connections = chip_solver.sort_connections(random_gate_connections)
        not_solved = chip_solver.run(sorted_random_connections, neighbor_lock_nr)

        # if all wires are placed the loop stops
        if not_solved == 0:
            # creates plot of solved netlist order
            chip_plot = Plot(grid)
            chip_plot.plot()
            return True

        # status update every thousand iterations
        if i % 100 == 0:
            print("Trying %d random orders of the netlist" % (iterations))
            print("Not solved: %d " % (not_solved))
            print("Iterations: %d" % (i))