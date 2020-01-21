from code.algorithms.random_priority import get_random_priority

def hill_climber(self, gate_connections):
        gate_connections = get_random_priority(gate_connections)
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