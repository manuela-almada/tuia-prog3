from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class UniformCostSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Uniform Cost Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Inicializamos un nodo con la posicion inicial
        nodo= Node("", grid.start, 0)

        frontera = PriorityQueueFrontier()
        frontera.add(nodo,nodo.cost)

        # Inicializamos el diccionario de explorados (vacio)
        explorado = {}
       
        # Add the node to the explored dictionary
        explorado[nodo.state] = nodo.cost

        while True:
            if frontera.is_empty():
                return NoSolution(explorado)
            # Removemos un nodo de la frontera
            nodo = frontera.pop()
            if nodo.state == grid.end:
                return Solution(nodo, explorado)
            sucesores = grid.get_neighbours(nodo.state)

           
            for accion, resultado in sucesores.items():  # Suponiendo que sucesores es un diccionario
                nuevo_estado = resultado
                costo_nuevo_estado=nodo.cost+ grid.get_cost(nuevo_estado)
               
                if nuevo_estado not in explorado or costo_nuevo_estado<explorado[nuevo_estado]:
                     # Inicializamos nodo hijo
                    nuevo_nodo = Node("", nuevo_estado,
                                    costo_nuevo_estado,
                                    parent=nodo,action=accion)
                   
                    explorado[nuevo_estado] = costo_nuevo_estado

                    frontera.add(nuevo_nodo,costo_nuevo_estado)

