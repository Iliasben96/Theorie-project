from code.heuristics.connection_amount import get_connections_per_gate

class NeighborLocker:

    def __init__(self, grid):
        self.grid = grid
        self.connections_per_gate = grid.connections_per_gate
        self.neighbor_gate_link = grid.neighbors_gates_link

    def get_available_neighbors_dict(self):
        
        available_neighbors_amounts = {}
        for gate,connection_amount in self.connections_per_gate.items():
            available_neighbors_amounts[gate] = 5 - connection_amount
        
        print(available_neighbors_amounts)
        return available_neighbors_amounts

    def get_all_gate_neighbors(self):
        print(self.neighbor_gate_link)

    def lock_neighbors(self, available_neighbors_amounts):

        hard_lock = {}
        for gate_nr,available_neighbor_amount in available_neighbors_amounts.items():
            if available_neighbor_amount == 0:
                gate = self.grid.gate_list[gate_nr - 1]
                neighbors_to_lock = self.grid.get_gate_neighbors(gate.coordinates)
                for neighbor in neighbors_to_lock:
                    hard_lock[neighbor] = gate_nr
        print(hard_lock)


    # Astar runt
    # Als je al bestaat, pak die state opnieuw
    # Zo niet
        # Pak de state van de vorige coordinaat
            # Als er geen vorige coordinaat is, kies begin state (Standaard grid, connections amount etc.)

    # Lock alle neighbors van alle gates die in de available neighbors amount (opgehaald uit state) op 0 staan
    # Unlock goal en start gates
    # Unlock alle neighbors van start en goal uit hard_lock (opgehaald uit state)
    # Ga een kant op
    # Check of dit nieuwe coordinaat een neighbor is, in neighbor gate link 
        # Zo ja, haal 1 af van de availible neighbors amount dict voor elke gate die deze neighbor bezit
        # Sla grid, coordinaat, available neighbors en hard_locks op in een state
        # Zo nee, doe niks
                

        