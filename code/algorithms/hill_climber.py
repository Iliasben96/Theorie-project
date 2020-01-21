from code.algorithms.random_priority import get_random_priority
from code.classes.chip_solver import ChipSolver

def hill_climber(grid, netlist, gate_connections):

        solved = False
        random_gate_connections = get_random_priority(gate_connections)
        cs = ChipSolver(grid, netlist)
        random_sorted_connections = cs.sort_connections(random_gate_connections)
        current_score = cs.make_connections(random_sorted_connections)
        if current_score == 0: 
            solved = True
        counter = 0 
        state = random_sorted_connections
        while solved == False and counter < 10:
            i = 0
            for connection in state:
                previous_state = state
                temp_priority = connection.priority 
                connection.priority = state[i + 1].priority
                state[i + 1].priority = temp_priority

                resorted_connections = cs.sort_connections(state)
                score = cs.make_connections(resorted_connections)
                if score == 0:
                    print("Yas, gelukt")
                    return state
                if score > current_score:
                    state = previous_state
                else: 
                    current_score = score
                i += 1




