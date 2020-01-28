from code.algorithms.astar import Astar
from code.heuristics.connection_length import get_connection_length_priority
from code.heuristics.random_priority import get_random_priority
from code.heuristics.connection_amount import get_amount_of_connections_priority
from code.heuristics.center_grid import get_priority_center_grid
from code.heuristics.z_up import Z_Up
from code.algorithms.random_loop import start_random_solutions
from code.classes.results_csv_generator import generate_results_csv

import operator

class ChipSolver:  
    """ Chipsolver creates a priority list for all connections from the netlist, 
    it calls A* to find the shortest path for each connection.
    User input is required to select a what heuristic to apply and what option to pick for neighborlocking
    """
    
    def __init__(self, grid, netlist):
        self.grid = grid
        self.netlist = netlist
        self.not_solved_counter = 0
        self.gate_connections = grid.gate_connections

    def sort_connections(self, gate_connections):
        """Sorts inputted gate_connections, based on the priority value of each connection"""

        sorted_connections = {}
        priority = 0

        # filters connections based on priority 
        for connection in (sorted(gate_connections.values(), key=operator.attrgetter('priority'))):
            # assigns heighest priority first in the list
            sorted_connections[priority] = connection
            priority += 1

        return sorted_connections

    def run(self, sorted_connections, neighbor_lock_nr):
        """Run Astar in the order of the sorted_connections, with the correct neighbor_lock_nr"""

        astar = Astar()
        not_solved_counter = 0

        # Loop over sorted connections
        for sorted_connection in sorted_connections.values():

            # Get a path from Astar algorithm
            path = astar.start(neighbor_lock_nr, self.grid, sorted_connection)
            
            # if A* can not place path +1 to the not_solved_counter
            if path == None:
                not_solved_counter += 1
            self.not_solved_counter = not_solved_counter

        return not_solved_counter

    def start(self, heuristic_nr, neighbor_lock_nr, z_up_option):
        """Start solving the chip with a heuristic number"""

        sorted_gate_connections = {}

        # Sandard netlist order
        if heuristic_nr == 1:
            sorted_gate_connections = self.sort_connections(self.gate_connections)


        # Connections with shorter length have priority
        if heuristic_nr == 2:
            prioritised_gate_connections = get_connection_length_priority(self.gate_connections)
            sorted_gate_connections = self.sort_connections(prioritised_gate_connections)

        # Netlist is ordered in a random fashion
        if heuristic_nr == 3:
            prioritised_gate_connections = get_random_priority(self.gate_connections)
            sorted_gate_connections = self.sort_connections(prioritised_gate_connections)


        # Netlist is ordered by the amount of connections, gates with most connections have priority
        if heuristic_nr == 4:
            prioritised_gate_connections = get_amount_of_connections_priority(self.netlist, self.gate_connections)
            sorted_gate_connections = self.sort_connections(prioritised_gate_connections)

        # Netlist is ordered based on what connections are shortest
        if heuristic_nr == 5:
            prioritised_gate_connections = get_priority_center_grid(self.grid, self.gate_connections)
            sorted_gate_connections = self.sort_connections(prioritised_gate_connections)

        # Try an amount of random netlist orders
        if heuristic_nr == 6:
            iterations = input("How many iterations do you want to try: ")
            while iterations.isdigit() == False:
                iterations = input("Error: please provide a number higher than zero: ")
            iterations = int(iterations)

            while iterations < 0:
                iterations = input("Error: please provide a number higher than zero: ")
            
            solved = start_random_solutions(self.grid, iterations, self)
            if solved == False:
                print("no solution found")
            else: 
                generate_results_csv(self.grid, self.netlist)

        # Select the z_up_option based on user input
        if z_up_option == True:
            z_up = Z_Up(sorted_gate_connections, self.grid, self.not_solved_counter)
            z_up.run(self.grid, neighbor_lock_nr)
            self.not_solved_counter = z_up.not_solved_counter
        else:
            self.run(sorted_gate_connections, neighbor_lock_nr)
