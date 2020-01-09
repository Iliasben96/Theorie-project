class Connection:

    def __init__(self, gate_a, gate_b, distance):
        self.gate_a = gate_a
        self.gate_b = gate_b
        self.distance = distance

    def __str__(self):
        return f'{self.distance}'