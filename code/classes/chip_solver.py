from code.algorithms.astar import astar
from code.heuristics.connection_length import get_connection_length_priority
from code.algorithms.random_priority import get_random_priority
from code.heuristics.connection_amount import get_amount_of_connections_priority
from code.heuristics.center_grid import get_priority_center_grid

import operator

class ChipSolver:  

    def __init__(self, grid, netlist):
        self.grid = grid
        self.netlist = netlist
        self.not_solved_counter = 0
        self.gate_connections = grid.gate_connections

    def sort_connections(self, gate_connections):
        sorted_connections = {}

        counter = 0
        for connection in (sorted(gate_connections.values(), key=operator.attrgetter('priority'))):
            sorted_connections[counter] = connection
            counter += 1

        return sorted_connections

    def make_connections(self, sorted_connections):

        not_solved_counter = 0

        for sorted_connection in sorted_connections:
            path = astar(self.grid, sorted_connection)
            # print(path)
            if path == None:
                not_solved_counter += 1
            self.not_solved_counter = not_solved_counter

        return not_solved_counter

    def start(self, option):
        if option == 1:
            sorted_gate_connections = self.sort_connections(self.gate_connections)
            self.make_connections(sorted_gate_connections)
        if option == 2:
            prioritised_gate_connections = get_connection_length_priority(self.gate_connections)
            sorted_gate_connections = self.sort_connections(prioritised_gate_connections)
            self.make_connections(sorted_gate_connections)
        if option == 3:
            prioritised_gate_connections = get_random_priority(self.gate_connections)
            sorted_gate_connections = self.sort_connections(prioritised_gate_connections)
            self.make_connections(sorted_gate_connections)
        if option == 4:

            prioritised_gate_connections = get_amount_of_connections_priority(self.netlist, self.gate_connections)
            sorted_gate_connections = self.sort_connections(prioritised_gate_connections)
            self.make_connections(sorted_gate_connections)
            self.make_connections(prioritised_gate_connections)
        if option == 5:
            prioritised_gate_connections = get_priority_center_grid(self.grid, self.gate_connections)
            sorted_gate_connections = self.sort_connections(prioritised_gate_connections)
            self.make_connections(sorted_gate_connections)