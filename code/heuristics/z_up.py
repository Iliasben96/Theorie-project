from code.algorithms.astar import Astar
from code.heuristics.connection_length import get_connection_length_priority
from code.heuristics.random_priority import get_random_priority
from code.heuristics.connection_amount import get_amount_of_connections_priority
from code.heuristics.center_grid import get_priority_center_grid


class Z_Up:
    """Class that tries to solve the chip as usual, if it finds that there are unsolved connections, 
    it bumps up all previous connections 1 up the z-axis and tries the unsolved connections again.
    """

    def __init__(self, sorted_connections, grid, not_solved_counter):
        self.sorted_connections = sorted_connections
        self.grid = grid
        self.not_solved_counter = not_solved_counter

    def can_raise(self, grid):
        """Check if the current connections can be raised, according to the maximum Z"""
        max_z = 6
        for connection in grid.wired_connections.values():
            path = connection["path"]
            for coordinate in path:  
                if coordinate[2] == max_z:
                    return False
        return True

    def increase_level(self, grid):
        """Function that increases level of all current connections"""

        # Place back connections that were removed as walkable due to Astar
        for connection in grid.wired_connections.values():
            path = connection["path"]
            for coordinate in path:
                grid.place_coordinate(coordinate)

        # Select correct wires, only wires that have a length more than 4 get their z incremented, 
        # as otherwise it does not free up space in a grid where only manhattan moves are allowed.
        for connection in grid.wired_connections.values():

            path = connection["path"]

            if len(path) > 4:
                second_wire = path[1]
                second_last_wire = path[-2]

                # Create new wire with added Z coördinate
                insert_third_wire_list = list(second_wire)
                insert_third_wire_list[2] += 1
                insert_third_wire = tuple(insert_third_wire_list)

                # Create new wire with added Z coördinate
                insert_third_last_wire_list = list(second_last_wire)
                insert_third_last_wire_list[2] += 1
                insert_third_last_wire = tuple(insert_third_last_wire_list)

                # Insert third and third to last wire
                path.insert(2, insert_third_wire)
                path.insert(-2, insert_third_last_wire)

                # Make sure added wires are represented in the wire_count
                grid.wire_count += 2

        # Increase Z coördinate of every cable between third and third to last wire
        for connection in grid.wired_connections.values():

            path = connection["path"]

            if len(path) > 4:
                counter = 0
                max_wires = len(path)
                for wire in path:
                    if (max_wires - 3) > counter and counter > 2:
                        list_wire = list(wire)
                        list_wire[2] += 1
                        insert_wire = tuple(list_wire)
                    else:
                        insert_wire = wire
                    path[counter] = insert_wire
                    counter += 1

        # Remove all coordinates from new connections from the grid, so Astar can't walk there anymore
        for connection in grid.wired_connections.values():
            path = connection["path"]
            for wire in path:
                grid.remove_coordinate(wire)

        return False



    def solver(self, neighbor_option, sorted_connections):
        """Try to solve the sorted connections with Astar"""

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

    def run(self, grid, neighbor_option):
        """Attempt to solve the chip normally, 
        bump up Z if connections are not laid, try again untill found solution, 
        the solution doesn't improve or grid can't be bumped up anymore
        """

        to_solve = self.sorted_connections
        not_solved = self.solver(neighbor_option, to_solve)
        self.not_solved_counter = len(not_solved)

        # Init previous not solved to have one more to come into the loop
        previous_not_solved = self.not_solved_counter + 1

        # keeps running until there are no unresolved connections
        while self.not_solved_counter != 0 and self.can_raise(grid) and previous_not_solved > self.not_solved_counter:

            self.increase_level(grid)

            previous_not_solved = self.not_solved_counter

            # tries to solve the unsolved connections after raising the level
            not_solved = self.solver(neighbor_option, not_solved) 
            self.not_solved_counter = len(not_solved)