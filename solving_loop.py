from priority_queue import PriorityQueue
from algorithms import Algorithms
from grid import Grid
import random

class SolvingLoop:  

    def __init__(self, grid, netlist):
        self.grid = grid
        self.netlist = netlist
        self.not_solved_counter = 0
        self.get_gate_links()

    # Make sure this list contains gate objects instead of tuples
    gate_links = []

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
        for connection in self.netlist:

            link = []

            # Get gate numbers from netlist
            gate_a_nr = connection[0]
            gate_b_nr = connection[1]

            # Get corresponding gates from gate_list
            start_gate = self.grid.gate_list[gate_a_nr - 1]
            goal_gate = self.grid.gate_list[gate_b_nr - 1]

            # Make a tuple from the gate object

            link.append(start_gate)
            link.append(goal_gate)

            self.gate_links.append(link)

    # Rebuild all functions to return priority instead of priority queue
    def get_priority_center_grid(self):

        algorithms = Algorithms()

        centre_x = abs(self.grid.grid_max_x / 2)
        centre_y = abs(self.grid.grid_max_y / 2)

        centre = (centre_x, centre_y, 0)

        # TODO: sort the connection based on the lowest manhattan heuristic
        for link in self.gate_links:
            start_gate = link[0]
            start_coordinate = start_gate.coordinates
            goal = centre
            priority = algorithms.manhattan_heuristic(start_coordinate, goal)
            start_gate.priority += priority


    def get_amount_of_connections_priority(self, connections_per_gate):

        for gate_nr,n_connections in connections_per_gate.items():

            priority = (6 - n_connections) / 2
            for link in self.gate_links:
                gate_a = link[0]
                gate_b = link[1]

                if gate_nr == gate_a.nr:
                    gate_a.priority += priority
                elif gate_nr == gate_b.nr:
                    gate_b.priority += priority              

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

        for link in self.gate_links:

            start_gate = link[0]
            goal_gate = link[1]
            start_coordinate = start_gate.coordinates
            goal_coordinate = goal_gate.coordinates

            priority = algorithms.manhattan_heuristic(start_coordinate, goal_coordinate)

            start_gate.priority += priority
        

    def solver(self, solving_queue):
        algorithms = Algorithms()

        not_solved_counter = 0

        while not solving_queue.empty():
            current_connection = solving_queue.get()
            path = algorithms.astar(self.grid, current_connection[0], current_connection[1])
            # print(path)
            if path == None:
                not_solved_counter += 1
        self.not_solved_counter = not_solved_counter

    def random_selector(self):
        priority = 1

        for link in self.netlist:
            option_list = random.choices(self.netlist, k=1)
            option = option_list[0]
            self.netlist.remove(option)
            gate_nr = option[0]
            gate = self.grid.gate_list[gate_nr - 1]
            gate.priority += priority
            priority += 1
            

    def start(self, priority_option):

        # Try to solve using lowest length first
        if priority_option == 1:
            self.get_connection_length_priority()
            pq = self.generate_pq()
            self.solver(pq)

        # Try to solve using closest to center first
        elif priority_option == 2:
            self.get_priority_center_grid()
            pq = self.generate_pq()
            self.solver(pq)

        # Try to solve using number of connections per gate first
        elif priority_option == 3:
            connections_per_gate = self.get_connections_per_gate()
            self.get_amount_of_connections_priority(connections_per_gate)
            pq = self.generate_pq()
            self.solver(pq)

        elif priority_option == 4:
            self.get_connection_length_priority()
            self.get_priority_center_grid()
            pq = self.generate_pq()
            self.solver(pq)

        elif priority_option == 5:
            pq = self.generate_pq()
            self.solver(pq)

        elif priority_option == 6:
            self.random_selector()
            pq = self.generate_pq()
            self.solver(pq)
        
    def get_grid(self):
        return self.grid
