from code.algorithms.astar import Astar
from code.heuristics.connection_length import get_connection_length_priority
from code.heuristics.random_priority import get_random_priority
from code.heuristics.connection_amount import get_amount_of_connections_priority
from code.heuristics.center_grid import get_priority_center_grid
from code.heuristics.z_up import Z_Up

import operator

class ChipSolver:  
    """ Chipsolver creates a priority list, it calls A* to create the paths needed for that list.
    User input is required to select the requested heuristic to run the loop.
    """
    
    def __init__(self, grid, netlist):
        self.grid = grid
        self.netlist = netlist
        self.not_solved_counter = 0
        self.gate_connections = grid.gate_connections

    def sort_connections(self, gate_connections):
        sorted_connections = {}

        counter = 0
        # filters connections based on priority 
        for connection in (sorted(gate_connections.values(), key=operator.attrgetter('priority'))):
            # assigns heighest priority first in the list
            sorted_connections[counter] = connection
            counter += 1

        return sorted_connections

    def run(self, sorted_connections, neighbor_option):

        astar = Astar()
        not_solved_counter = 0

        for sorted_connection in sorted_connections.values():
            path = astar.start(neighbor_option, self.grid, sorted_connection)
            # if A* can not place path +1 to the not_solved_counter
            if path == None:
                not_solved_counter += 1
            self.not_solved_counter = not_solved_counter

        return not_solved_counter

    def start(self, option, neighbor_option):

        # standard netlist order
        if option == 1:
            sorted_gate_connections = self.sort_connections(self.gate_connections)
            self.run(sorted_gate_connections, neighbor_option)

        # calls the function to prioritse connections based on length
        if option == 2:
            prioritised_gate_connections = get_connection_length_priority(self.gate_connections)
            sorted_gate_connections = self.sort_connections(prioritised_gate_connections)
            self.run(sorted_gate_connections, neighbor_option)

        # calls the random function, orders netlist in a random order
        if option == 3:
            prioritised_gate_connections = get_random_priority(self.gate_connections)
            sorted_gate_connections = self.sort_connections(prioritised_gate_connections)
            self.run(sorted_gate_connections, neighbor_option)

        # calls the connection amount function, which gives priority based on amount of connections
        if option == 4:
            prioritised_gate_connections = get_amount_of_connections_priority(self.netlist, self.gate_connections)
            sorted_gate_connections = self.sort_connections(prioritised_gate_connections)
            self.run(sorted_gate_connections, neighbor_option)
            self.run(prioritised_gate_connections, neighbor_option)

        # calls the priority_centergrid function, which orders chips based on their distance from the center of the grid
        if option == 5:
            prioritised_gate_connections = get_priority_center_grid(self.grid, self.gate_connections)
            sorted_gate_connections = self.sort_connections(prioritised_gate_connections)
            self.run(sorted_gate_connections, neighbor_option)

        # uses the 
        if option == 7:
            prioritised_gate_connections = get_amount_of_connections_priority(self.netlist, self.gate_connections)
            sorted_gate_connections = self.sort_connections(prioritised_gate_connections)
            z_up = Z_Up(sorted_gate_connections, self.grid, self.not_solved_counter)
            z_up.run(neighbor_option)
            self.not_solved_counter = z_up.not_solved_counter