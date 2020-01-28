class Connection:
    """Connection class that holds the connection between 2 gates 
    gate_a and gate_b are gate objects (see code/classes/gate.py), connection_id as integer
    and priority, to later sort which connections goes first
    """

    def __init__(self, gate_a, gate_b, connection_id):
        self.gate_a = gate_a
        self.gate_b = gate_b
        self.connection_id = connection_id
        self.priority = 0