# Class that stores the number and coordinates of a gate

class Gate:

    def __init__(self, nr, coordinates, connection_amount):
        self.nr = nr
        self.coordinates = coordinates
        self.priority = 0
        self.connection_amount = connection_amount 
        self.neighbors = []

    def __str__(self):
        return f'nr: {self.nr} coordinates: {self.coordinates}'