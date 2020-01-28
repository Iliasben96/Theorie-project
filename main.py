from code.classes.netlist_reader import netlistreader
from code.classes.grid import Grid
from code.visualisation.plot import Plot
from code.classes.chip_solver import ChipSolver
from code.classes.results_csv_generator import generate_results_csv
from code.user_interface.user_interface import get_user_chip_nr, get_user_netlist_nr, get_user_heuristic_nr, get_user_neighbor_lock_nr, get_z_up

    
def main():
    """Main function that runs the programme that attempts to solve the Chips & Circuits case"""

    # Get user inputs
    chip_nr = get_user_chip_nr()
    netlist_nr = get_user_netlist_nr(chip_nr)
    heuristic_nr = get_user_heuristic_nr()
    z_up_option = get_z_up()
    neighbor_lock_nr = get_user_neighbor_lock_nr()

    # Use netlistreader to read the provided netlist csv
    netlist = netlistreader(chip_nr,netlist_nr)

    # Make new grid instance
    grid = Grid(chip_nr, netlist, neighbor_lock_nr)

    # Make new chip solver instance
    chip_solver = ChipSolver(grid, netlist)
    chip_solver.start(heuristic_nr, neighbor_lock_nr, z_up_option)

    # Get total connections from the length of the netlist
    total_connections = len(netlist)

    # Solution information
    print("Wires not solved %d " % (chip_solver.not_solved_counter))
    print("Wires solved %d" % (total_connections - chip_solver.not_solved_counter))
    print("Wires used: %d" % (grid.wire_count))
    wires_per_connection = grid.wire_count / (total_connections - chip_solver.not_solved_counter)
    print("Wires per succesfull connection")
    print(wires_per_connection)

    # Generates visual plot for the gates and their connections
    chip_plot = Plot(grid)
    chip_plot.plot()

    # Generate a table that holds all found paths for each connection in the netlist
    generate_results_csv(grid, netlist)

if __name__ == "__main__":
    main()