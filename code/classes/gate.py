class Gate:
    """Class that stores the number as integer, coordinates as tuple (x, y, z) 
    and connection_amount as an integer ranging from 0 to 5
    """
    def __init__(self, nr, coordinates, connection_amount):
        self.nr = nr
        self.coordinates = coordinates
        self.connection_amount = connection_amount 
