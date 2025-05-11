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
        # Inicializamos el nodo de partida
        nodo_inicio = Node("", grid.start, 0)
       
        #  explorado es el diccionario para rastrear los estados visitados
        explorado = {}
        explorado[nodo_inicio.state] = True

        # Inicializamos la frontera utilizando una cola de prioridad f = g + h
        frontera = PriorityQueueFrontier()
        h = AStarSearch.manhattan(grid.start, grid.end)
        f = nodo_inicio.cost + h
        frontera.add(nodo_inicio, f)

        # Bucle principal
        while not frontera.is_empty():
            #Quitamos el nodo con el menor costo total
            nodo_actual = frontera.pop()

            # Chequea si el estado actual es el estado objetivo
            if nodo_actual.state == grid.end:
                return Solution(nodo_actual, explorado)

            # Explora a los vecinos
            for accion, nuevo_estado in grid.get_neighbours(nodo_actual.state).items():
                if nuevo_estado not in explorado:
                    # Calcula el costo para alcanzar a este vecino
                    g = nodo_actual.cost + grid.get_cost(nuevo_estado)
                    h = AStarSearch.manhattan(nuevo_estado, grid.end)
                    f = g + h

                    # Crea el nuevo nodo
                    nodo_hijo = Node("",nuevo_estado, g, parent=nodo_actual, action=accion)

                    # Marcar el nuevo estado como explorado
                    explorado[nuevo_estado] = True

                    # Añadimos el nodo a la frontera con su prioridad
                    frontera.add(nodo_hijo, f)

        #Si no se encuentra camino
        return NoSolution(explorado)