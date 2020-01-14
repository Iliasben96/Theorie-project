import math
from grid import Grid
from priority_queue import PriorityQueue

class Node:

    def pythagoras_heuristic(self, current, goal):
        a = current[0] - goal[0] 
        b = current[1] - goal[1]
        z_heuristic = abs(current[2] - goal[2])

        h_squared = a**2 + b**2 

        h = math.sqrt(h_squared) + z_heuristic

        return h

    def manhattan_heuristic(self, current, goal):
        
        distance_x = abs(current[0]- goal[0])
        distance_y = abs(current[1] - goal[1])
        distance_z = abs(current[2] - goal[2])

        h = distance_x + distance_y + (distance_z * 2)
        return h
        
    # Shortest path algorithm Dijkstra 
    def astar(self, grid, start, goal):

        # Initialise the priority queue
        frontier = PriorityQueue()

        # Put start in the queue
        frontier.put(start, 0)

        # Initialise an archive
        came_from = {}

        # The total cost so far
        cost_so_far = {}

        # Initialse start with a came from of None
        came_from[start] = None
        cost_so_far[start] = 0

        # Explore map untill queue is empty
        while not frontier.empty():

            # Get first item in priority queue
            current = frontier.get()

            # Stop if you reach goal
            if current == goal:
                print("Found goal")

                position = current
                while position != came_from[start]:
                    print(position)
                    grid.put_wire(position)
                    position = came_from[position]
                    

                break

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
                    priority = new_cost + self.manhattan_heuristic(next_node, goal)

                    # Put child in prioriy queue
                    frontier.put(next_node, priority)

                    # Store where the child came from
                    came_from[next_node] = current
