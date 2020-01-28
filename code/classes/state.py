class State:
    """State class to store the state of the neighbors that Astar can't walk provided it's path.
    Used by the runtime neighborlocking version of Astar
    """

    def __init__(self, coordinates, locked_neighbors, available_neighbors_amount):
        self.coordinates = coordinates
        self.locked_neighbors = locked_neighbors
        self.available_neighbors_amount = available_neighbors_amount