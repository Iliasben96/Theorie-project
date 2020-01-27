import math
from code.classes.grid import Grid
from code.classes.priority_queue import PriorityQueue
from code.heuristics.manhattan import manhattan_heuristic
from code.classes.state import State
from code.heuristics.neighbor_locker import NeighborLocker

# Shortest path algorithm Astar 
def astar(grid, connection):
    """ A* algorithm to search for the shortest possible distance for a wire, using manhattan distance.
    It uses heuristics to determine the order of the wires and to decide how to use neighbors.
    """

    start_gate = connection.gate_a
    goal_gate = connection.gate_b

    start_coordinates = start_gate.coordinates
    goal_coordinates = goal_gate.coordinates
    # Make sure start and end are walkable
    grid.add_start_end_gates(start_coordinates, goal_coordinates)

    if grid.remove_neighbors == True:
        grid.add_back_gate_neighbors(start_coordinates, goal_coordinates)

    # Initialise the priority queue
    frontier = PriorityQueue()

    # Put start in the queue
    frontier.put(start_coordinates, 0)

    # Initialise an archive
    came_from = {}

    # The total cost so far
    cost_so_far = {}

    state_dict = {}

    # Initialse start with a came from of None
    came_from[start_coordinates] = None
    cost_so_far[start_coordinates] = 0

    nl = NeighborLocker(grid)

    all_gate_neighbors = nl.get_all_gate_neighbors()

    available_neighbors = nl.get_available_neighbors_dict()
    print(available_neighbors)

    locked_neighbors = nl.lock_neighbors(available_neighbors, {}, start_gate.nr, goal_gate.nr)

    # print(locked_neighbors)
    state = State(start_coordinates, locked_neighbors, available_neighbors)

    counter = 0
    # Explore map untill queue is empty
    while not frontier.empty():

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
                

        print("State: %d" % (counter))
        counter += 1

        # if counter == 5:
        #     break

        # Get first item in priority queue
        current = frontier.get()

        # Stop if you reach goal
        if current == goal_coordinates:
            # print("Found goal")
            path = []
            position = current
            while position != came_from[start_coordinates]:
                path.append(position)
                grid.all_wires.append(position)
                position = came_from[position] 
            grid.put_connection(path)      
            print("Found solution")
            return path

        print(current)

        # If the current state exists in the dict already, fetch it
        if current in state_dict:
            state = state_dict[start_coordinates]
            print("Coordinate exists already")

        # If it is not, get the previous state as the current state
        else:
            print("Coordinate doesn't exist yet")
            if came_from[current] in state_dict:

                print("Previous coordinate does exist")
                state = state_dict[came_from[current]]
            elif came_from[state.coordinates] == None:

                print("Made first node")
                state_dict[current] = state 

        # Get available neighbors
        available_neighbors = state.available_neighbors_amount

        print("Available neighbors:")
        print(available_neighbors)

        # Lock neighbors that need to be locked
        locked_neighbors = nl.lock_neighbors(available_neighbors, state.locked_neighbors, start_gate.nr, goal_gate.nr)

        print("Locked neighbors: ")
        print(locked_neighbors)


        # If the current is a neighbor of a gate, and not locked
        if current in all_gate_neighbors and current not in locked_neighbors:

            neighbors_to_use = all_gate_neighbors[current]

            # Loop over list of gates that have this neighbor
            for gate_nr in neighbors_to_use:

                # Check if the gate has an open spot in available gate neigbors
                if gate_nr in available_neighbors and available_neighbors[gate_nr] > 0:
                        print("Coordinate is neighbor of gate %d, one is deducted from it's free spots" % (gate_nr))

                        # If it has an available spot, 
                        temp = available_neighbors[gate_nr]
                        temp -= 1
                        available_neighbors[gate_nr] = temp
        
        # Save any and all changes in a new state
        new_state = State(current, locked_neighbors, available_neighbors)


        print("Saved to new state with values")
        print(current)
        print(locked_neighbors)
        print(available_neighbors)
        state = new_state

        # Store this new state in a dict, with the current coordinate as a key
        state_dict[current] = state

        # Get neighbors from grid
        neighbors = grid.get_neighbors(current)

        
        # Loop over neighbors of current node
        for next_node in neighbors:

            # Only move to a next node if it isn't locked
            if next_node not in locked_neighbors:

                # Calculate new cost for each neighbor
                new_cost = cost_so_far[current] + 1

                # See if next node is already visited or if the cost 
                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    
                    # Store the cost so far
                    cost_so_far[next_node] = new_cost

                    # Add priority
                    priority = new_cost + manhattan_heuristic(next_node, goal_coordinates)

                    # Put child in prioriy queue
                    frontier.put(next_node, priority)

                    # Store where the child came from
                    came_from[next_node] = current

    if grid.remove_neighbors == True:
        grid.relock_gate_neighbors(start_coordinates, goal_coordinates)