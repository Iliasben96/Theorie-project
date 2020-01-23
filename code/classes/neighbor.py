class Neighbor:

    def __init__(self, nr, coordinates):
        self.nr = nr
        self.coordinates = coordinates

    def __str__(self):
        return f'nr: {self.nr} coordinates: {self.coordinates}'

