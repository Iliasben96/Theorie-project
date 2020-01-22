from code.classes.grid import Grid
from code.visualisation.plot import Plot
from code.classes.chip_solver import ChipSolver
from code.heuristics.random_priority import get_random_priority


def start_random_solutions(chip_nr, netlist, remove_neighbors, iterations):
    for i in range(iterations):

        grid = Grid(chip_nr, netlist, remove_neighbors)
        cs = ChipSolver(grid, netlist)
        random_gate_connections = get_random_priority(cs.gate_connections)
        sorted_random_connections = cs.sort_connections(random_gate_connections)
        not_solved = cs.make_connections(sorted_random_connections)

        if not_solved == 0:
            print("Success")
            print("Found solution on %d iteration" % (i))
            print(grid.connections_list)
            chip_plot = Plot(grid)
            chip_plot.plot()
            return True

        
        if i % 1000 == 0:
            print("Trying %d random orders of the netlist" % (iterations))
            print("Not solved: %d " % (not_solved))
            print("Iterations: %d" % (i))
        
    


        