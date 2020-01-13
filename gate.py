class Gate:

    def __init__(self, nr, x, y):
        self.nr = nr
        self.x = x
        self.y = y

    def __str__(self):
        return f'nr: {self.nr} x: {self.x} y:{self.y}'