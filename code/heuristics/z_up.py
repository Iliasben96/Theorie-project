from code.algorithms.astar import astar
from code.heuristics.connection_length import get_connection_length_priority
from code.heuristics.random_priority import get_random_priority
from code.heuristics.connection_amount import get_amount_of_connections_priority
from code.heuristics.center_grid import get_priority_center_grid


class Z_Up:

    def __init__(self, sorted_connections, grid, not_solved_counter):
        self.sorted_connections = sorted_connections
        self.grid = grid
        self.not_solved_counter = not_solved_counter

    def solver(self, sorted_connections):

        unsolved_dict = {}
        i = 0

        # Put unsolved connections in dict
        for sorted_connection in sorted_connections.values():
            path = astar(self.grid, sorted_connection)
            if path == None:
                unsolved_dict[i] = sorted_connection
                self.not_solved_counter += 1
                # print(i)
                i += 1
                # print(sorted_connection.gate_a)
                # print(sorted_connection.gate_b)
        return unsolved_dict

    def run(self):

        counter = 0
        to_solve = self.sorted_connections
        not_solved = self.solver(to_solve)
        while not_solved != False:
            if counter > 1:
                print("Oeps, out of bounds")
                break
            self.grid.increase_level()
            not_solved = self.solver(not_solved)
            counter += 1
        self.not_solved_counter = len(not_solved)