class Wire:    
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f'x: {self.x} y:{self.y} z: {self.z}'