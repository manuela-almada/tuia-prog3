from ..models.grid import Grid
from ..models.frontier import StackFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class DepthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Depth First Search

        Args:
            grid (Grid): Grid of points
           
        Returns:
            Solution: Solution found
        """
        # Inicializamos un nodo como posicion inicial
        nodo = Node("", grid.start, 0)

        # Inicializamos el diccionario de explorados
        explorado = {}
       
        #Test-Objetivo
        if nodo.state == grid.end:
            return Solution(nodo, explorado)
           
        frontera = StackFrontier()
        frontera.add(nodo)

        while True:

            #  Falla si la frontera esta vacia
            if frontera.is_empty():
                return NoSolution(explorado)
            # Removemos un nodo de la frontera
            nodo = frontera.remove()
           

            if nodo.state in explorado:
                continue
            explorado[nodo.state]=True
            sucesores = grid.get_neighbours(nodo.state)

            for accion, resultado in sucesores.items():  
                nuevo_estado = resultado  # Obtener el nuevo estado


                # Chequeamos si el sucesor no ha sido explorado
                if nuevo_estado not in explorado:

                        # Initializamos el nodo hijo
                    nuevo_nodo = Node("", nuevo_estado,
                                        nodo.cost + grid.get_cost(nuevo_estado),
                                        parent=nodo,action=accion)
                        # Marcamos el sucesor como alcanzado
                    #explorado[nuevo_estado] = True

                    # Retornamos si el nodo posee un estado objetivo
                    if nuevo_estado == grid.end:
                        return Solution(nuevo_nodo, explorado)
               
                 
                    # Aniadimos el nuevo nodo a la frontera
                    frontera.add(nuevo_nodo)