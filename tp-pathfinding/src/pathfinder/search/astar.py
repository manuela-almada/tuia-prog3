from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class AStarSearch:
    @staticmethod
    def manhattan(pos1: tuple[int, int], pos2: tuple[int, int]) -> int:
        """Compute Manhattan distance between two positions"""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using A* Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found or not
        """
        # Initialize the start node
        start_node = Node("", grid.start, 0)
        
        # Explored dictionary to track visited states
        explored = {}
        explored[start_node.state] = True

        # Initialize the frontier as a priority queue using f = g + h
        frontier = PriorityQueueFrontier()
        h = AStarSearch.manhattan(grid.start, grid.end)
        f = start_node.cost + h
        frontier.add(start_node, f)

        # Main loop
        while not frontier.is_empty():
            # Remove node with the lowest total cost
            current_node = frontier.pop()

            # Check if goal is reached
            if current_node.state == grid.end:
                return Solution(current_node, explored)

            # Explore neighbors
            for action, new_state in grid.get_neighbours(current_node.state).items():
                if new_state not in explored:
                    # Calculate cost to reach this neighbor
                    g = current_node.cost + grid.get_cost(new_state)
                    h = AStarSearch.manhattan(new_state, grid.end)
                    f = g + h

                    # Create the new node
                    child_node = Node("", new_state, g, parent=current_node, action=action)

                    # Mark it as explored
                    explored[new_state] = True

                    # Add to the frontier with its priority
                    frontier.add(child_node, f)

        # If no path is found
        return NoSolution(explored)
    