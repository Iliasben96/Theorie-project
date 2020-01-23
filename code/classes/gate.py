# Class that stores the number and coordinates of a gate

class Gate:

    def __init__(self, nr, coordinates, connection_amount):
        self.nr = nr
        self.coordinates = coordinates
        self.priority = 0
        self.connection_amount = connection_amount 
        self.used_neighbors = 0
        self.neighbors = []

    def __str__(self):
        return f'nr: {self.nr} coordinates: {self.coordinates}'

    def get_available_connections(self):
        max_connections = 5
        available_connections = max_connections - self.connection_amount

        if available_connections == 0:
            return available_connections
        else: 
            return available_connections - self.used_neighbors

