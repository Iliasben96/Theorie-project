import math
from code.classes.grid import Grid
from code.classes.priority_queue import PriorityQueue
from code.heuristics.manhattan import manhattan_heuristic
from code.heuristics.neighbor_locker import NeighborLocker
from code.classes.state import State

# Shortest path algorithm Astar 
def astar(grid, connection):

    start_gate = connection.gate_a
    goal_gate = connection.gate_b

    start_coordinates = start_gate.coordinates
    goal_coordinates = goal_gate.coordinates
    # Make sure start and end are walkable
    grid.add_start_end_gates(start_coordinates, goal_coordinates)

    if grid.remove_neighbors == True:
        grid.neighbor_locker.add_back_gate_neighbors(grid, start_gate, goal_gate)

    # Initialise the priority queue
    frontier = PriorityQueue()

    # Put start in the queue
    frontier.put(start_coordinates, 0)

    # Initialise an archive
    came_from = {}

    # The total cost so far
    cost_so_far = {}

    # Initialse start with a came from of None
    came_from[start_coordinates] = None
    cost_so_far[start_coordinates] = 0

    grid_of_path = {}
    
    temp_grid = grid

    gate_list = temp_grid.gate_list

    neighbor_locker = NeighborLocker(temp_grid, gate_list)

    gate_connections_dict = neighbor_locker.make_gate_connections_dict(gate_list)

    state = State(start_coordinates, gate_connections_dict, neighbor_locker.closed_neighbors, temp_grid)

    # Explore map untill queue is empty
    while not frontier.empty():

        # Get first item in priority queue
        current = frontier.get()

        if current in grid_of_path:
            state = grid_of_path[current]
        else:
            if came_from[current] in grid_of_path:
                state = grid_of_path[came_from[current]]
                print("Current node:" )
                print(current)
                print("I came from")
                print(came_from[current])
            elif came_from[current] == None:
                print("I am the start node")
                print(current)

        # TODO: Use this later
        
        new_gate_list = neighbor_locker.check_if_neighbor(current, state.grid, state.gate_list)

        closed_list = neighbor_locker.lock_gate_neighbors(state.grid, state.gate_list)

        new_state = State(current, new_gate_list, closed_list, temp_grid)

        grid_of_path[current] = new_state

        print(state)
        print(new_state)

        # Stop if you reach goal
        if current == goal_coordinates:
            path = []
            position = current
            while position != came_from[start_coordinates]:
                path.append(position)
                grid.all_wires.append(position)
                position = came_from[position] 
            grid.put_connection(path)     
            start_gate.connection_amount -= 1
            goal_gate.connection_amount -= 1
            print(grid.neighbor_locker.closed_neighbors)
            return path

        # Get neighbors from grid
        neighbors = temp_grid.get_neighbors(current)
        
        # Loop over neighbors of current node
        for next_node in neighbors:

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
        grid.neighbor_locker.relock_gate_neighbors(grid, start_gate, goal_gate)