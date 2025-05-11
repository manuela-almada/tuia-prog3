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
        # Inicializamos el nodo inicial
        nodo_inicial = Node("", grid.start, 0)
       
        # Diccionario de explorado para rastrear estados ya alcanzados
        explorado = {}
        explorado[nodo_inicial.state] = True

        # Inicializamos la frontera como una cola de prioridad utilizando distancia de Manhattan
        frontera = PriorityQueueFrontier()
        prioridad = GreedyBestFirstSearch.manhattan(nodo_inicial.state, grid.end)
        frontera.add(nodo_inicial, prioridad)

        # Bucle principal
        while not frontera.is_empty():
            # Removemos el nodo con menor heuristica (prioridad)
            nodo_actual = frontera.pop()

            # Realizamos el test objetivo
            if nodo_actual.state == grid.end:
                return Solution(nodo_actual, explorado)

            # Exploramos a los vecinos
            for accion, nuevo_estado in grid.get_neighbours(nodo_actual.state).items():
                if nuevo_estado not in explorado:
                    costo = nodo_actual.cost + grid.get_cost(nuevo_estado)
                    nodo_hijo = Node("", nuevo_estado, costo, parent=nodo_actual, action=accion)
                    explorado[nuevo_estado] = True
                    prioridad = GreedyBestFirstSearch.manhattan(nuevo_estado, grid.end)
                    frontera.add(nodo_hijo, prioridad)

        # Si el test objetivo nunca fue alcanzado
        return NoSolution(explorado)