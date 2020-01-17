from priority_queue import PriorityQueue
from algorithms import Algorithms
from grid import Grid
import random
from connection import Connection

class TestSolver:  

    def __init__(self, grid, netlist):
        self.grid = grid
        self.netlist = netlist
        self.not_solved_counter = 0

    # Make sure this list contains gate objects instead of tuples
    connections = {}

    def make_connections(self):
        id_counter = 0
        for connection in self.netlist:

            # Get gate numbers from netlist
            gate_a_nr = connection[0]
            gate_b_nr = connection[1]

            # Get corresponding gates from gate_list
            start_gate = self.grid.gate_list[gate_a_nr - 1]
            goal_gate = self.grid.gate_list[gate_b_nr - 1]

            new_connection = Connection(start_gate, goal_gate, id_counter)
            self.connections[id_counter] = new_connection
            id_counter += 1