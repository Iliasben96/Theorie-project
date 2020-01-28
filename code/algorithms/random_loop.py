from code.classes.grid import Grid
from code.visualisation.plot import Plot
from code.classes.chip_solver import ChipSolver
from code.heuristics.random_priority import get_random_priority


def start_random_solutions(chip_nr, netlist, remove_neighbors, iterations, neighbor_option):
    """ A loop to run the random algorithm over the netlist
    After generating a random order of the netlist the paths are put and the algorithm checks if solutions are found. 
    This process repeats until the maximun iterations is reached or a solution is found.
    """

    # loops for the amount of iterations the user specified
    for i in range(iterations):
        
        # runs the alogrithm for a random order of the netlist
        grid = Grid(chip_nr, netlist, remove_neighbors)
        cs = ChipSolver(grid, netlist)
        random_gate_connections = get_random_priority(cs.gate_connections)
        sorted_random_connections = cs.sort_connections(random_gate_connections)
        not_solved = cs.run(sorted_random_connections, neighbor_option)

        # if all wires are placed the loop stops
        if not_solved == 0:
            print("Success")
            print("Found solution on %d iteration" % (i))
            print(grid.connections_list)

            # creates plot of solved netlist order
            chip_plot = Plot(grid)
            chip_plot.plot()
            return True

        # status update every thousand iterations
        if i % 100 == 0:
            print("Trying %d random orders of the netlist" % (iterations))
            print("Not solved: %d " % (not_solved))
            print("Iterations: %d" % (i))
        
    


        