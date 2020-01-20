from algorithms import Algorithms
from grid import Grid
import random
from connection import Connection
import operator

class SolvingLoop:  

    def __init__(self, grid, netlist):
        self.grid = grid
        self.netlist = netlist
        self.not_solved_counter = 0
        self.gate_connections = {}
        self.make_connections()

        # Make sure this list contains gate objects instead of tuples

<<<<<<< HEAD
    # Create tuple from gate object
    def debug(self):
        print (self.gate_links)

        # start_position = (start_gate.x, start_gate.y, start_gate.z)
        # goal_position = (goal_gate.x, goal_gate.y, goal_gate.z)
        return

    def generate_pq(self):

        pq = PriorityQueue()
        for link in self.gate_links:
            tuple_link = []

            gate_start = link[0]
            gate_goal = link[1]
            gate_start_position = gate_start.coordinates
            gate_goal_position = gate_goal.coordinates

            tuple_link.append(gate_start_position)
            tuple_link.append(gate_goal_position)

            pq.put(tuple_link, gate_start.priority)
        return pq

    def get_gate_links(self):
=======

    def make_connections(self):
        id_counter = 0
>>>>>>> test
        for connection in self.netlist:

            # Get gate numbers from netlist
            gate_a_nr = connection[0]
            gate_b_nr = connection[1]

            # Get corresponding gates from gate_list
            start_gate = self.grid.gate_list[gate_a_nr - 1]
            goal_gate = self.grid.gate_list[gate_b_nr - 1]

<<<<<<< HEAD
            # Make a tuple from the gate object

            link.append(start_gate)
            link.append(goal_gate)

            self.gate_links.append(link)
=======
            new_connection = Connection(start_gate, goal_gate, id_counter)
            self.gate_connections[id_counter] = new_connection
            id_counter += 1
>>>>>>> test

    # Rebuild all functions to return priority instead of priority queue
    def get_priority_center_grid(self):

        algorithms = Algorithms()

        centre_x = abs(self.grid.grid_max_x / 2)
        centre_y = abs(self.grid.grid_max_y / 2)

        centre = (centre_x, centre_y, 0)

        # TODO: sort the connection based on the lowest manhattan heuristic
<<<<<<< HEAD
        for link in self.gate_links:
            start_gate = link[0]
            start_coordinate = start_gate.coordinates
            goal = centre
            priority = algorithms.manhattan_heuristic(start_coordinate, goal)
            start_gate.priority += priority
=======
        for connection_nr in self.gate_connections:
            connection = self.gate_connections[connection_nr]
            gate_a = connection.gate_a
            gate_b = connection.gate_b
>>>>>>> test

            gate_a_priority = algorithms.manhattan_heuristic(gate_a.coordinates, centre)
            gate_b_priority = algorithms.manhattan_heuristic(gate_b.coordinates, centre)

            priority = (gate_a_priority + gate_b_priority) / 2
            connection.priority = priority

    def get_amount_of_connections_priority(self, connections_per_gate):

        for gate_nr,n_connections in connections_per_gate.items():

            priority = (6 - n_connections) / 2
<<<<<<< HEAD
            for link in self.gate_links:
                gate_a = link[0]
                gate_b = link[1]

                if gate_nr == gate_a.nr:
                    gate_a.priority += priority
                elif gate_nr == gate_b.nr:
                    gate_b.priority += priority              

=======
            for connection_nr in self.gate_connections:
                connection = self.gate_connections[connection_nr]
                gate_a = connection.gate_a
                gate_b = connection.gate_b

                if gate_nr == gate_a.nr or gate_nr == gate_b.nr:
                    connection.priority += priority
           
>>>>>>> test
    def get_connections_per_gate(self):

        gate_n_connections = {}


        # Calculate priority for each connection based on number of connections
        for connection in self.netlist:

            # Get gate numbers from netlist
            gate_a_nr = connection[0]
            gate_b_nr = connection[1]

            # Count number of connections per gate
            if gate_a_nr in gate_n_connections.keys():
                gate_n_connections[gate_a_nr] += 1
            else: 
                gate_n_connections[gate_a_nr] = 1
            if gate_b_nr in gate_n_connections.keys():
                gate_n_connections[gate_b_nr] += 1
            else:
                gate_n_connections[gate_b_nr] = 1

        # Sorting dictionary from: https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
        # Sort dictionary based on number of connections, highest first
        sorted_gate_n_connections = {k: v for k, v in sorted(gate_n_connections.items(), key=lambda item: item[1], reverse=True)}
        return sorted_gate_n_connections   

    def get_connection_length_priority(self):
        algorithms = Algorithms()

        # Calculate priority for each connection

<<<<<<< HEAD
        for link in self.gate_links:

            start_gate = link[0]
            goal_gate = link[1]
            start_coordinate = start_gate.coordinates
            goal_coordinate = goal_gate.coordinates
=======
         # TODO: sort the connection based on the lowest manhattan heuristic
        for connection_nr in self.gate_connections:
            connection = self.gate_connections[connection_nr]
            gate_a = connection.gate_a
            gate_b = connection.gate_b
>>>>>>> test

            priority = algorithms.manhattan_heuristic(gate_a.coordinates, gate_b.coordinates)

            connection.priority += priority
        

    def solver(self):
        algorithms = Algorithms()

        not_solved_counter = 0

        sorted_connections = []

        for connection in (sorted(self.gate_connections.values(), key=operator.attrgetter('priority'))):
            sorted_connections.append(connection)

        for sorted_connection in sorted_connections:
            gate_a = sorted_connection.gate_a
            gate_b = sorted_connection.gate_b

            gate_a_coordinates = gate_a.coordinates
            gate_b_coordinates = gate_b.coordinates

            path = algorithms.astar(self.grid, gate_a_coordinates, gate_b_coordinates)
            # print(path)
            if path == None:
                not_solved_counter += 1
            self.not_solved_counter = not_solved_counter

    def random_selector(self):

        connection_numbers = []
        for connection_nr in self.gate_connections.keys():
            connection_numbers.append(connection_nr)
        random.shuffle(connection_numbers)

        counter = 0
        for connection_nr in connection_numbers:

            connection = self.gate_connections[counter]
            connection.priority = connection_numbers[connection_nr]
            print(connection.priority)
            counter += 1

    def get_grid(self):
        return self.grid
