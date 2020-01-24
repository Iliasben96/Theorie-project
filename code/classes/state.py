class State:

    def __init__(self, position, gate_list, closed_neighbors, grid):
        self.position = position
        self.gate_list = gate_list
        self.closed_neighbors = closed_neighbors
        self.grid = grid

    def __str__(self):
        return f'Position: {self.position}'
