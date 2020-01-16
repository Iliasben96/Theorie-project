from priority_queue import PriorityQueue
from algorithms import Algorithms
from grid import Grid

class SolvingLoop:  

    def __init__(self, grid, netlist):
        self.grid = grid
        self.netlist = netlist
        self.get_gate_links()

    gate_links = []


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
            start_position = (start_gate.x, start_gate.y, start_gate.z)
            goal_position = (goal_gate.x, goal_gate.y, goal_gate.z)

            link.append(start_position)
            link.append(goal_position)

            SolvingLoop.gate_links.append(link)


    def get_priority_center_grid(self):
        pq = PriorityQueue()

        algorithms = Algorithms()

        centre_x = abs(self.grid.grid_max_x / 2)
        centre_y = abs(self.grid.grid_max_y / 2)

        centre = (centre_x, centre_y, 0)

        for link in SolvingLoop.gate_links:
            start = link[0]
            goal = centre

            priority = algorithms.manhattan_heuristic(start, goal)
            pq.put(link, priority)
        return pq

            
        

        # voor elke gate:
        # krijg manhattan afstand tussen gate en center
        # Gooi gates met deze afstand als prioriteit in priority queue

    def get_amount_of_connections_priority(self, connections_per_gate):

        pq = PriorityQueue()
        queue = []
        for gate_nr, gate_connections in connections_per_gate.items():
        
            for gate_connection in gate_connections:
                if gate_connection in self.netlist:
                    queue.append(gate_connection)
                    self.netlist.remove(gate_connection)

        for connection in queue:
            
            link = []

            chip_a = connection[0]
            chip_b = connection[1]

            start_gate = self.grid.gate_list[chip_a - 1]
            goal_gate = self.grid.gate_list[chip_b -1]

            start_position = (start_gate.x, start_gate.y, start_gate.z)
            goal_position = (goal_gate.x, goal_gate.y, goal_gate.z)

            link.append(start_position)
            link.append(goal_position)
            pq.put(link, 1)


        return pq

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
        

        connections_per_gate = sorted_gate_n_connections

        for gate_nr,connections  in connections_per_gate.items():
        
            # List to store all connections of one specific gate
            gate_connections = []


            for link in self.netlist:

                # Check if current gate is either chip_a or chip_b in current connection
                if gate_nr in link:
                    
                    gate_connections.append(link)
        
            # Add list of all connections of one chip to dictionary
            connections_per_gate[gate_nr] = gate_connections

        return connections_per_gate

    def get_connection_length_priority(self):
        algorithms = Algorithms()

        solving_queue = PriorityQueue()

        # Calculate priority for each connection

        for link in SolvingLoop.gate_links:

            start_position = link[0]
            goal_position = link[1]
            h = algorithms.manhattan_heuristic(start_position, goal_position)

            solving_queue.put(link, h)
        return solving_queue

    def solver(self, solving_queue):
        algorithms = Algorithms()

        not_solved_counter = 0

        while not solving_queue.empty():
            current_connection = solving_queue.get()
            path = algorithms.astar(self.grid, current_connection[0], current_connection[1])
            # print(path)
            if path == None:
                not_solved_counter += 1
        print("%d wrong connections" % (not_solved_counter))

    def start(self, priority_option):
        if priority_option == 1:
            pq = self.get_connection_length_priority()
            self.solver(pq)

        elif priority_option == 2:
            connections_per_gate = self.get_connections_per_gate()
            pq = self.get_amount_of_connections_priority(connections_per_gate)
            self.solver(pq)
        elif priority_option == 3:
            pq = self.get_priority_center_grid()
            self.solver(pq)
