from ..models.grid import Grid
from ..models.frontier import QueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class BreadthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Breadth First Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found or not found
        """
        # Initialize the frontier with the starting node
        start_node = Node("", grid.start, 0)
        frontier = QueueFrontier()
        frontier.add(start_node)

        # Dictionary to track explored positions
        explored = {start_node.state: True}

        while not frontier.is_empty():
            # Remove a node from the frontier (FIFO order)
            node = frontier.remove()

            # Check if we've reached the goal
            if node.state == grid.end:
                return Solution(node, explored)

            # Get neighbors (valid movements and resulting positions)
            neighbours = grid.get_neighbours(node.state)

            for action, pos in neighbours.items():
                if pos not in explored:
                    # Create a new node for the neighbor
                    new_node = Node(
                        value="",                 # Not used here
                        state=pos,                # New position
                        cost=node.cost + grid.get_cost(pos),  # Cost to reach this node
                        parent=node,              # Link to parent node
                        action=action             # Action taken to reach this node
                    )

                    # Add new node to the frontier
                    frontier.add(new_node)

                    # Mark position as explored
                    explored[pos] = True

        # No solution found
        return NoSolution(explored)
