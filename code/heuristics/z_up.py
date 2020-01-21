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

        self.increased_level = False
        if path == None and self.increased_level == False:
            self.grid.increase_level()
            self.increased_level = True
            not_solved_counter += 1
        if path == None and self.increased_level == True:
            not_solved_counter += 1
        self.not_solved_counter = not_solved_counter