"""Este modulo define la clase LocalSearch.

LocalSearch representa un algoritmo de busqueda local general.

Las subclases que se encuentran en este modulo son:

* HillClimbing: algoritmo de ascension de colinas. Se mueve al sucesor con
mejor valor objetivo. Ya viene implementado.

* HillClimbingReset: algoritmo de ascension de colinas de reinicio aleatorio.
No viene implementado, se debe completar.

* Tabu: algoritmo de busqueda tabu.
No viene implementado, se debe completar.
"""


from __future__ import annotations
from time import time
from problem import OptProblem


class LocalSearch:
    """Clase que representa un algoritmo de busqueda local general."""

    def __init__(self) -> None:
        """Construye una instancia de la clase."""
        self.niters = 0  # Numero de iteraciones totales
        self.time = 0  # Tiempo de ejecucion
        self.tour = []  # Solucion, inicialmente vacia
        self.value = None  # Valor objetivo de la solucion

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion."""
        self.tour = problem.init
        self.value = problem.obj_val(problem.init)


class HillClimbing(LocalSearch):
    """Clase que representa un algoritmo de ascension de colinas.

    En cada iteracion se mueve al estado sucesor con mejor valor objetivo.
    El criterio de parada es alcanzar un optimo local.
    """

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion con ascension de colinas.

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimizacion
        """
        # Inicio del reloj
        start = time()

        # Arrancamos del estado inicial
        actual = problem.init
        value = problem.obj_val(problem.init)

        while True:

            # Buscamos la acción que genera el sucesor con mayor valor objetivo
            act, succ_val = problem.max_action(actual)

            # Retornar si estamos en un maximo local:
            # el valor objetivo del sucesor es menor o igual al del estado actual
            if succ_val <= value:

                self.tour = actual
                self.value = value
                end = time()
                self.time = end-start
                return

            # Sino, nos movemos al sucesor
            actual = problem.result(actual, act)
            value = succ_val
            self.niters += 1


class HillClimbingReset(LocalSearch):
    """Algoritmo de ascension de colinas con reinicio aleatorio."""
    
    def __init__(self,niters_ant =0,time_ant =0) -> None:
        super().__init__()
        self.max_iteraciones=200
    
    def solve(self, problem:OptProblem):
        # Inicio del reloj
        start = time()

        # Arrancamos del estado inicial
        actual = problem.init
        value = problem.obj_val(problem.init)
        mejor_tour=actual
        mejor_value=value
        reinicios_realizados=0

        while reinicios_realizados<self.max_iteraciones:
            while True:

                # Buscamos la acción que genera el sucesor con mayor valor objetivo
                act, succ_val = problem.max_action(actual)

                # Retornar si estamos en un maximo local:
                # el valor objetivo del sucesor es menor o igual al del estado actual
                if succ_val <= value:
                    break

                # Sino, nos movemos al sucesor
                actual = problem.result(actual, act)
                value = succ_val
                self.niters += 1
            if value>mejor_value:
                mejor_tour=actual
                mejor_value=value
            actual=problem.random_reset()
            value=problem.obj_val(actual)
            reinicios_realizados+=1


        self.tour=mejor_tour
        self.value=mejor_value

        end = time()
        self.time = end-start
        return


class Tabu(LocalSearch):
    """Algoritmo de busqueda tabu."""

    def __init__(self) -> None:
        """Inicializa el algoritmo Tabú.
       
        Argumentos:
        ==========
        max_iters: int
            Número máximo de iteraciones que se ejecutará la búsqueda Tabú.
       
        tabu_size: int
            El tamaño máximo de la lista Tabú. Una vez alcanzado este tamaño,
            se eliminarán las acciones más antiguas.
        """
        super().__init__()
        self.max_iters = 1000  # Número máximo de iteraciones
        self.tabu_size = 20  # Tamaño máximo de la lista Tabú
        self.tabu_list = []  # Lista de acciones Tabú


    def solve(self, problem: OptProblem) -> None:
        """Resuelve un problema de optimización usando la búsqueda Tabú.
       
        Argumentos:
        ==========
        problem: OptProblem
            El problema de optimización a resolver.
        """
        # Inicializamos el estado
        estado_actual = problem.init
        valor_actual = problem.obj_val(estado_actual)
        mejor_tour = estado_actual
        mejor_valor = valor_actual
       
        # Iniciamos el reloj
        start_time = time()
       
        # Número de iteraciones
        iteraciones = 0

        while iteraciones < self.max_iters:
            # Buscamos la mejor acción posible que no esté en la lista tabú
            action, succ_value = problem.max_action(estado_actual, self.tabu_list,mejor_valor)
           
            # Si encontramos una mejor solución, actualizamos la mejor
            if valor_actual > mejor_valor:
                mejor_tour = estado_actual
                mejor_valor = valor_actual
               
            # Añadimos la acción a la lista tabú
            self.tabu_list.append(action)
               
            # Si la lista tabú supera el tamaño máximo, eliminamos la acción más antigua
            if len(self.tabu_list) > self.tabu_size:
                self.tabu_list.pop(0)  # Eliminamos el primer elemento, el más antiguo

            estado_actual = problem.result(estado_actual, action)
            valor_actual = succ_value   
            # Incrementamos el contador de iteraciones
            iteraciones += 1
            

        # Establecemos el mejor tour y el valor encontrado
        self.tour = mejor_tour
        self.value = mejor_valor
        self.time = time() - start_time  # Tiempo total de ejecución
        self.niters = iteraciones  # Número total de iteraciones
