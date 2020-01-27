class State:

    def __init__(self, coordinates, locked_neighbors, available_neighbors_amount):
        self.coordinates = coordinates
        self.locked_neighbors = locked_neighbors
        self.available_neighbors_amount = available_neighbors_amount