# Class that stores the number and coordinates of a gate

class Gate:

    def __init__(self, nr, x, y):
        self.nr = nr
        self.x = x
        self.y = y
        self.z = 0

    def __str__(self):
        return f'nr: {self.nr} x: {self.x} y:{self.y} z:{self.z}'