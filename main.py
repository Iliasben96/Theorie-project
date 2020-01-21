from code.classes.netlist_reader import netlistreader
from code.classes.grid import Grid
from code.classes.gate import Gate
from code.visualisation.plot import Plot
from code.classes.solving_loop import SolvingLoop

if __name__ == "__main__":

    chip_nr = input("Please choose the chip number: (1 or 2) ")

    while chip_nr.isdigit() == False:
        chip_nr = input("Error: please input either 1 or 2: ")

    chip_nr = int(chip_nr)
    while chip_nr < 0 or chip_nr > 2:
        chip_nr = input("Error please input either 1 or 2: ")

    chip_nr = int(chip_nr)

    if chip_nr == 1:

        netlist_nr = input("Please choose netlist number (1, 2, or 3): ")

        while netlist_nr.isdigit() == False:
            netlist_nr = input("Error: please choose netlist number (1, 2, or 3): ")
        
        netlist_nr = int(netlist_nr)
        while netlist_nr < 0 or netlist_nr > 3:
            netlist_nr = input("Error: please choose netlist number (1, 2, or 3): ")
    
    if chip_nr == 2:
        netlist_nr = input("Please choose netlist number (4, 5, or 5): ")

        while netlist_nr.isdigit() == False:
            netlist_nr = input("Error: please choose netlist number (4, 5, or 6): ")
        
        netlist_nr = int(netlist_nr)
        while netlist_nr < 4 or netlist_nr > 6:
            netlist_nr = input("Error: please choose netlist number (4, 5, or 6): ")
    
    heuristic_nr = input("What heuristics do you want to run? \n 1: none, 2: connection_length, 3: random, 4: amount of connections, 5: center grid: ")     

    while heuristic_nr.isdigit() == False:
        heuristic_nr = input("Error: please choose heuristic number (1 through 5): ")
    
    heuristic_nr = int(heuristic_nr)
    while heuristic_nr < 0 or netlist_nr > 5:
        netlist_nr = input("Error: please choose heuristic number (1 through 5): ")

    netlist = netlistreader(chip_nr,netlist_nr)

    # # Make new grid instance
    grid = Grid(chip_nr, netlist, True)

    sl = SolvingLoop(grid, netlist)
    # connections_per_gate = sl.get_connections_per_gate()

    sl.start(heuristic_nr)

    print("Wires not solved %d " % (sl.not_solved_counter))
    print("Wires solved %d" % (30 - sl.not_solved_counter))
    print("Wires used: %d" % (grid.wire_count))
    wires_per_connection = grid.wire_count / (30 - sl.not_solved_counter)
    print("Wires per succesfull connection")
    print(wires_per_connection)

    chip_plot = Plot(grid)
    chip_plot.plot()