from estado_cuantico import EstadoCuantico
from typing import List
from typing import Dict, Union
import numpy as np
class OperadorCuantico:
    def __init__(self, nombre, matriz):
        """
        Clase que representa un operador cuántico (matriz unitaria).
        :param nombre: Nombre o etiqueta del operador (por ejemplo, "X", "H").
        :param matriz: Matriz que implementa la transformación lineal (lista de listas).
        """
        self.nombre = nombre
        self.matriz = np.array(matriz, dtype=complex)

    def aplicar(self, estado):
        """
        Aplica el operador cuántico a un estado cuántico.
        :param estado: Instancia de EstadoCuantico.
        :return: Nuevo EstadoCuantico con el estado transformado.
        """
        nuevo_vector = np.dot(self.matriz, estado.vector)
        nuevo_id = f"{estado.id}_{self.nombre}"
        return EstadoCuantico(nuevo_id, nuevo_vector, estado.base)


# Pruebas
if __name__ == "__main__":
    # Estado inicial |0>
    estado = EstadoCuantico("q0", [1, 0], "computacional")

    # Operador X (NOT cuántico)
    opX = OperadorCuantico("X", [[0, 1], [1, 0]])
    nuevo_estado_X = opX.aplicar(estado)
    print(nuevo_estado_X)  # Debería representar |1> = [0, 1]
    print(nuevo_estado_X.vector)  # Esperado: [0, 1]

    # Operador H (Hadamard)
    opH = OperadorCuantico("H", [[1/np.sqrt(2), 1/np.sqrt(2)], [1/np.sqrt(2), -1/np.sqrt(2)]])
    nuevo_estado_H = opH.aplicar(estado)
    print(nuevo_estado_H)  # Debería representar un estado aproximadamente [0.707, 0.707]
    print(nuevo_estado_H.vector)  # Esperado: [0.707, 0.707]