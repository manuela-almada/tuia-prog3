from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class GreedyBestFirstSearch:
    @staticmethod
    def manhattan(pos1: tuple[int, int], pos2: tuple[int, int]) -> int:
        """Compute Manhattan distance between two points"""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Greedy Best First Search

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

        # Initialize the frontier as a priority queue using Manhattan distance
        frontier = PriorityQueueFrontier()
        priority = GreedyBestFirstSearch.manhattan(start_node.state, grid.end)
        frontier.add(start_node, priority)

        # Main search loop
        while not frontier.is_empty():
            # Remove the node with the lowest heuristic (priority)
            current_node = frontier.pop()

            # Check if goal is reached
            if current_node.state == grid.end:
                return Solution(current_node, explored)

            # Explore neighbors
            for action, new_state in grid.get_neighbours(current_node.state).items():
                if new_state not in explored:
                    cost = current_node.cost + grid.get_cost(new_state)
                    child_node = Node("", new_state, cost, parent=current_node, action=action)
                    explored[new_state] = True
                    priority = GreedyBestFirstSearch.manhattan(new_state, grid.end)
                    frontier.add(child_node, priority)

        # If the goal was never reached
        return NoSolution(explored)