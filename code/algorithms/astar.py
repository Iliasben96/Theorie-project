import math
from code.classes.grid import Grid
from code.classes.priority_queue import PriorityQueue
from code.heuristics.manhattan import manhattan_heuristic

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

    # Explore map untill queue is empty
    while not frontier.empty():

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
            return path
        
        grid.neighbor_locker.check_if_neighbor(current, grid)

        grid.neighbor_locker.lock_gate_neighbors(grid)

        # Get neighbors from grid
        neighbors = grid.get_neighbors(current)
        
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