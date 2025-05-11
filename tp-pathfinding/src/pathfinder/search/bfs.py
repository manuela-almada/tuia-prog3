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
        # Inicializamos la frontera (COLA) con el nodo incial
        nodo_inicial = Node("", grid.start, 0)
        frontera = QueueFrontier()
        frontera.add(nodo_inicial)

        # Diccionario para rastrear estados explorados
        explorado = {nodo_inicial.state: True}

        while not frontera.is_empty():
            # Removemos un nodo de la frontera
            nodo = frontera.remove()

            # Chequeamos si llegamos al objetivo
            if nodo.state == grid.end:
                return Solution(nodo, explorado)

            # Obtener vecinos (acciones validas y  estados resultantes)
            vecinos = grid.get_neighbours(nodo.state)

            for accion, resultado in vecinos.items():
                if resultado not in explorado:
                    # Creamos un nodo nuevo para el vecino
                    nuevo_nodo = Node(
                        value="",
                        state=resultado,
                        cost=nodo.cost + grid.get_cost(resultado),
                        parent=nodo,
                        action=accion
                    )

                    # Aniadimos el nuevo nodo a la frontera
                    frontera.add(nuevo_nodo)

                    # Marcamos la posicion como explorado
                    explorado[resultado] = True

        # Si no se encontro solucion:
        return NoSolution(explorado)
