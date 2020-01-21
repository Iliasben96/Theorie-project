from code.classes.grid import Grid
from code.classes.connection import Connection
from code.algorithms.astar import astar
from code.heuristics.manhattan import manhattan_heuristic
from code.heuristics.connection_length import get_connection_length_priority
from code.algorithms.random_priority import get_random_priority
from code.heuristics.connection_amount import get_amount_of_connections_priority
from code.heuristics.center_grid import get_priority_center_grid

import random
import operator

class SolvingLoop:  

    def __init__(self, grid, netlist):
        self.grid = grid
        self.netlist = netlist
        self.not_solved_counter = 0
        self.gate_connections = grid.gate_connections

    def solver(self, gate_connections):

        not_solved_counter = 0

        sorted_connections = []

        # Make gate.connections an argument of this method
        for connection in (sorted(gate_connections.values(), key=operator.attrgetter('priority'))):
            sorted_connections.append(connection)

        for sorted_connection in sorted_connections:
            path = astar(self.grid, sorted_connection)
            # print(path)
            if path == None:
                not_solved_counter += 1
            self.not_solved_counter = not_solved_counter

        return sorted_connections

    def start(self, option):
        if option == 1:
            self.solver(self.gate_connections)
        if option == 2:
            gate_connections = get_connection_length_priority(self.gate_connections)
            self.solver(gate_connections)
        if option == 3:
            gate_connections = get_random_priority(self.gate_connections)
            self.solver(gate_connections)
        if option == 4:
            gate_connections = get_amount_of_connections_priority(self.netlist, self.gate_connections)
            self.solver(gate_connections)
        if option == 5:
            gate_connections = get_priority_center_grid(self.grid, self.gate_connections)
            self.solver(gate_connections)

    def get_grid(self):
        return self.grid