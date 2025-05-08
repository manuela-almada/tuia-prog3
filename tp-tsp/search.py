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
    """
    Algoritmo de Ascensión de Colinas con Reinicio Aleatorio.

    Esta versión realiza múltiples búsquedas locales desde diferentes
    estados aleatorios, con el objetivo de evitar caer en óptimos locales
    subóptimos y encontrar mejores soluciones globales.
    """

    def __init__(self, restarts=20):
        """
        Inicializa el algoritmo con la cantidad deseada de reinicios.

        Parámetros:
        -----------
        restarts : int
            Cantidad de reinicios aleatorios a ejecutar (default: 20).
        """
        super().__init__()
        self.restarts = restarts  # Total de reinicios del algoritmo

    def solve(self, problem: OptProblem):
        """
        Ejecuta el algoritmo Hill Climbing con múltiples reinicios aleatorios.

        En cada reinicio:
        - Se parte de un estado aleatorio generado por `random_reset()`.
        - Se aplica ascensión de colinas clásica hasta quedar atrapado en un óptimo local.
        - Se guarda la mejor solución encontrada a lo largo de todos los reinicios.

        Parámetros:
        -----------
        problem : OptProblem
            Instancia del problema de optimización que se desea resolver.
        """
        from time import time

        start_time = time()  # Comenzamos a medir el tiempo
        best_state = None
        best_value = float('-inf')

        for _ in range(self.restarts):
            # Reinicio: comenzar desde un estado aleatorio
            current = problem.random_reset()
            current_value = problem.obj_val(current)

            while True:
                # Buscar la mejor acción aplicable desde el estado actual
                action, next_value = problem.max_action(current)

                # Si no mejora, llegamos a un óptimo local
                if next_value <= current_value:
                    break

                # Aplicar acción y moverse al nuevo estado
                current = problem.result(current, action)
                current_value = next_value
                self.niters += 1  # Contabilizar iteración

            # Actualizar mejor solución global si fue superada
            if current_value > best_value:
                best_state = current
                best_value = current_value

        # Guardar los resultados finales
        self.tour = best_state
        self.value = best_value
        self.time = time() - start_time


class Tabu(LocalSearch):
    """Algoritmo de búsqueda Tabú para el problema del TSP."""
    
    def __init__(self, max_iters: 1000, tabu_size: 50) -> None:
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
        self.max_iters = max_iters  # Número máximo de iteraciones
        self.tabu_size = tabu_size  # Tamaño máximo de la lista Tabú
        self.tabu_list = []  # Lista de acciones Tabú

    def solve(self, problem: OptProblem) -> None:
        """Resuelve un problema de optimización usando la búsqueda Tabú.
        
        Argumentos:
        ==========
        problem: OptProblem
            El problema de optimización a resolver.
        """
        # Inicializamos el estado
        current_state = problem.init
        current_value = problem.obj_val(current_state)
        best_state = current_state
        best_value = current_value
        
        # Iniciamos el reloj
        start_time = time()
        
        # Número de iteraciones
        iter_count = 0

        while iter_count < self.max_iters:
            # Buscamos la mejor acción posible que no esté en la lista tabú
            action, succ_value = problem.max_action(current_state, self.tabu_list)
            
            # Si el valor objetivo de la acción sucesora es mejor, la tomamos
            if succ_value > current_value:
                # Aplicamos la acción
                current_state = problem.result(current_state, action)
                current_value = succ_value

                # Si encontramos una mejor solución, actualizamos la mejor
                if current_value > best_value:
                    best_state = current_state
                    best_value = current_value
                
                # Añadimos la acción a la lista tabú
                self.tabu_list.append(action)
                
                # Si la lista tabú supera el tamaño máximo, eliminamos la acción más antigua
                if len(self.tabu_list) > self.tabu_size:
                    self.tabu_list.pop(0)  # Eliminamos el primer elemento, el más antiguo
                
            # Incrementamos el contador de iteraciones
            iter_count += 1

        # Establecemos el mejor tour y el valor encontrado
        self.tour = best_state
        self.value = best_value
        self.time = time() - start_time  # Tiempo total de ejecución
        self.niters = iter_count  # Número total de iteraciones

