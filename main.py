from netlist_reader import netlistreader
from grid import Grid
from gate import Gate
from plot import Plot
from algorithms import Algorithms

if __name__ == "__main__":

    # Make new grid instance
    start_grid = Grid()

    # Generate start grid
    # TODO: Make this dynamic according to size of print
    grid = start_grid.get_start_grid(1, 25)

    netlist = netlistreader(1, 1)

    # Main loop to attempt to solve all connections in netlist
    for connection in netlist:
        
        algorithms = Algorithms()

        # Get corresponding gates from gate_list
        start_gate = start_grid.gate_list[connection[0] - 1]
        goal_gate = start_grid.gate_list[connection[1] - 1]

        # Make a tuple from the gate object
        start_position = (start_gate.x, start_gate.y, start_gate.z)
        goal_position = (goal_gate.x, goal_gate.y, goal_gate.z)

        path = algorithms.astar(start_grid, start_position, goal_position)
        print(path)
    
    # Create new plot
    chip_plot = Plot(start_grid)
    
    # Show new plot
    chip_plot.plot()