import heapq

# Retrieved from https://www.redblobgames.com/pathfinding/a-star/implementation.html
class PriorityQueue:
    """Priority queue used by Astar to determine which coordinates to explore first based on their heuristic value"""

    def __init__(self):
        self.elements = []

    def empty(self):
        """Returns True if the priorityqueue is empty"""

        return len(self.elements) == 0

    def put(self, item, priority):
        """Puts an item in the priorityqueue. It's put in order according to it's priority"""

        heapq.heappush(self.elements, (priority, item))

    def get(self):
        """Get first element, thus element with the lowest priority, from the priorityqueue"""

        return heapq.heappop(self.elements)[1]