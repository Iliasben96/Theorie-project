from code.classes.grid import Grid
from code.classes.connection import Connection
from code.algorithms.algorithms import Algorithms

import random
import operator

class SolvingLoop:  

    def __init__(self, grid, netlist):
        self.grid = grid
        self.netlist = netlist
        self.not_solved_counter = 0
        self.gate_connections = {}
        self.make_connections()
        self.connection_numbers = []

        # Make sure this list contains gate objects instead of tuples


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
            self.gate_connections[id_counter] = new_connection
            id_counter += 1

    # Rebuild all functions to return priority instead of priority queue
    def get_priority_center_grid(self):

        algorithms = Algorithms()

        centre_x = abs(self.grid.grid_max_x / 2)
        centre_y = abs(self.grid.grid_max_y / 2)

        centre = (centre_x, centre_y, 0)

        # TODO: sort the connection based on the lowest manhattan heuristic
        for connection_nr in self.gate_connections:
            connection = self.gate_connections[connection_nr]
            gate_a = connection.gate_a
            gate_b = connection.gate_b

            gate_a_priority = algorithms.manhattan_heuristic(gate_a.coordinates, centre)
            gate_b_priority = algorithms.manhattan_heuristic(gate_b.coordinates, centre)

            priority = (gate_a_priority + gate_b_priority) / 2
            connection.priority = priority

    def get_amount_of_connections_priority(self, connections_per_gate):

        for gate_nr,n_connections in connections_per_gate.items():

            priority = (6 - n_connections) / 2
            for connection_nr in self.gate_connections:
                connection = self.gate_connections[connection_nr]
                gate_a = connection.gate_a
                gate_b = connection.gate_b

                if gate_nr == gate_a.nr or gate_nr == gate_b.nr:
                    connection.priority += priority
           
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

         # TODO: sort the connection based on the lowest manhattan heuristic
        for connection_nr in self.gate_connections:
            connection = self.gate_connections[connection_nr]
            gate_a = connection.gate_a
            gate_b = connection.gate_b

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

        return sorted_connections

    def random_selector(self):

        for connection_nr in self.gate_connections.keys():
            self.connection_numbers.append(connection_nr)
        random.shuffle(self.connection_numbers)

        counter = 0
        for connection_nr in self.connection_numbers:

            connection = self.gate_connections[counter]
            connection.priority = self.connection_numbers[connection_nr]
            counter += 1

    def get_grid(self):
        return self.grid

    def hill_climber(self):
        self.random_selector()
        ordered_connection_list = self.solver()
        not_solved_counter = 0 
        current_best_solution = len(self.netlist)
        solution_found = False
        while solution_found == False:
            if solution_found == False:
                for j in range(len(ordered_connection_list)):
                    if solution_found == False:
                        for i in range(len(ordered_connection_list)):
                            temp_order = ordered_connection_list
                            temp_order[j], temp_order[i] = temp_order[i], temp_order[j]
                            counter = 0
                            for connection_nr in temp_order:
                                connection = self.gate_connections[counter]
                                connection.priority = self.connection_numbers[connection_nr]
                                counter += 1
                            
                            # output van solver met aantal mislukte connecties voor de connection
                            
                            if not_solved_counter < current_best_solution:
                                current_best_solution = not_solved_counter
                                ordered_connection_list = temp_order
                            
                            if current_best_solution == 0:
                                print("solution Found")
                                solution_found = True
                                break
                            

                    



        # self.random_selector()
        # ordered_connection_list = self.solver()
        # algorithms = Algorithms()
        # not_solved_counter = 0
        # current_best_solution = len(self.netlist)
        # solution_found = False
        # while current_best_solution != 0:
        #     # For connection in ordered_connection_list
        #     for j in range(len(ordered_connection_list)):
        #         if solution_found == False:
        #             for i in range(len(ordered_connection_list)):
        #                 if ordered_connection_list[j] != ordered_connection_list[i]:
        #                     temp_order = ordered_connection_list
        #                     temp_order[j], temp_order[i] = temp_order[i], temp_order[j]
        #                     if solution_found == False:
        #                         for connection in temp_order:
        #                             gate_a = connection.gate_a
        #                             gate_b = connection.gate_b

        #                             gate_a_coordinates = gate_a.coordinates
        #                             gate_b_coordinates = gate_b.coordinates

        #                             path = algorithms.astar(self.grid, gate_a_coordinates, gate_b_coordinates)

        #                             if path == None:
        #                                 not_solved_counter += 1

        #                             if not_solved_counter < current_best_solution:
        #                                 current_best_solution = not_solved_counter
        #                                 ordered_connection_list = temp_order
        #                                 print("improved")
                                    
        #                                 for connection in ordered_connection_list:
        #                                     print(connection)
        #                                 print(current_best_solution)

        #                             if current_best_solution == 0:
        #                                 print("solution found")
        #                                 solution_found = True
        #                                 break
        #                     else:
        #                         break
        
        # voor het eerst getal in de eerste iteratie wil ik alle andere oplossingen bekijken als ik deze en een andere wissel van plek
        # na het checken van alle opties voor deze iteratie selecteer een de beste van alle opties(als er een verbetering is)
        # maak de nieuwe volgorde met die list de base grid en selecteer de tweede in de lijst etc
        # tot er een oplossing is gevonden
                
                


            

    