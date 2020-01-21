class Connection:

    def __init__(self, gate_a, gate_b, connection_id):
        self.gate_a = gate_a
        self.gate_b = gate_b
        self.connection_id = connection_id
        self.priority = 0
    
    def __str__(self):
        return f'gate a: {self.gate_a}, gate b: {self.gate_b}'