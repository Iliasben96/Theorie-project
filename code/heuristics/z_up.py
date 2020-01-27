from code.algorithms.astar import Astar
from code.heuristics.connection_length import get_connection_length_priority
from code.heuristics.random_priority import get_random_priority
from code.heuristics.connection_amount import get_amount_of_connections_priority
from code.heuristics.center_grid import get_priority_center_grid


class Z_Up:

    def __init__(self, sorted_connections, grid, not_solved_counter):
        self.sorted_connections = sorted_connections
        self.grid = grid
        self.not_solved_counter = not_solved_counter

    def solver(self, neighbor_option, sorted_connections):
        astar = Astar()
        unsolved_dict = {}
        i = 0

        # runs A* for every connection
        for sorted_connection in sorted_connections.values():
            path = astar.start(neighbor_option, self.grid, sorted_connection)
            
            # if no connection can be found places the connection in the unsolved dictionary
            if path == None:
                unsolved_dict[i] = sorted_connection
                self.not_solved_counter += 1
                i += 1

        return unsolved_dict

    def run(self, neighbor_option):

        counter = 0
        to_solve = self.sorted_connections
        not_solved = self.solver(neighbor_option, to_solve)
        # keeps running until there are no unresolved connections
        while not_solved != False:

            # raise level function can only be used once
            if counter > 2:
                print("Oeps, out of bounds")
                break

            # runs the increase level funtion
            self.grid.increase_level()

            # tries to solve the unsolved connections after raising the level
            not_solved = self.solver(neighbor_option, not_solved)
            counter += 1
        
        self.not_solved_counter = len(not_solved)