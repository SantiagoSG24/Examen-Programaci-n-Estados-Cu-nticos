from typing import List, Dict, Union
import math
import numpy as np
import json
import json

class EstadoCuantico:
    def __init__(self, id: str, vector: List[complex], base: str):
        if not vector:
            raise ValueError("El vector de estado no puede estar vacío.")
        if not math.isclose(sum(abs(amplitud)**2 for amplitud in vector), 1.0, rel_tol=1e-9):
            raise ValueError("El vector de estado debe estar normalizado.")
        
        self.id = id
        self.vector = vector
        self.base = base

    def medir(self) -> Dict[str, float]:
        """Calcula las probabilidades de medición de cada estado base."""
        probabilidades = {str(i): abs(amplitud)**2 for i, amplitud in enumerate(self.vector)}
        return probabilidades

    def __str__(self) -> str:
        return f"{self.id}: vector={self.vector} en base {self.base}"

    def __repr__(self) -> str:
        return self.__str__()











        class OperadorCuantico:
            def __init__(self, id: str, matriz: List[List[complex]]):
                if not matriz or not all(len(fila) == len(matriz) for fila in matriz):
                    raise ValueError("La matriz debe ser cuadrada y no vacía.")
                if not np.allclose(np.dot(matriz, np.conjugate(np.transpose(matriz))), np.eye(len(matriz))):
                    raise ValueError("La matriz debe ser unitaria.")
                
                self.id = id
                self.matriz = np.array(matriz)

            def aplicar(self, estado: EstadoCuantico) -> EstadoCuantico:
                if len(estado.vector) != len(self.matriz):
                    raise ValueError("El tamaño del vector de estado no coincide con el tamaño de la matriz del operador.")
                
                nuevo_vector = np.dot(self.matriz, estado.vector)
                return EstadoCuantico(f"{estado.id}_{self.id}", nuevo_vector.tolist(), estado.base)

            def __str__(self) -> str:
                return f"Operador {self.id}: matriz={self.matriz}"

            def __repr__(self) -> str:
                return self.__str__()


        class RepositorioDeEstados:
            def __init__(self):
                self.estados = {}

            def listar_estados(self) -> List[str]:
                return [str(estado) for estado in self.estados.values()]

            def agregar_estado(self, id: str, vector: List[complex], base: str):
                if id in self.estados:
                    raise ValueError(f"Ya existe un estado con el id '{id}'.")
                self.estados[id] = EstadoCuantico(id, vector, base)

            def obtener_estado(self, id: str) -> EstadoCuantico:
                if id not in self.estados:
                    raise ValueError(f"No se encontró un estado con el id '{id}'.")
                return self.estados[id]

            def aplicar_operador(self, id_estado: str, op: OperadorCuantico, nuevo_id: str = None):
                estado = self.obtener_estado(id_estado)
                nuevo_estado = op.aplicar(estado)
                nuevo_estado.id = nuevo_id if nuevo_id else nuevo_estado.id
                self.estados[nuevo_estado.id] = nuevo_estado

            def medir_estado(self, id: str) -> Dict[str, float]:
                estado = self.obtener_estado(id)
                return estado.medir()

            def guardar(self, archivo: str):
                with open(archivo, 'w') as f:
                    json.dump({id: {"vector": estado.vector, "base": estado.base} for id, estado in self.estados.items()}, f)

            def cargar(self, archivo: str):
                with open(archivo, 'r') as f:
                    datos = json.load(f)
                    for id, info in datos.items():
                        self.agregar_estado(id, info["vector"], info["base"])





                        if __name__ == "__main__":
                            repositorio = RepositorioDeEstados()

                            # Agregar estados cuánticos al repositorio
                            repositorio.agregar_estado("q1", [1/np.sqrt(2), 1/np.sqrt(2)], "computacional")
                            repositorio.agregar_estado("q2", [1, 0], "computacional")

                            # Listar estados
                            print("Estados en el repositorio:")
                            for estado in repositorio.listar_estados():
                                print(estado)

                            # Medir un estado
                            print("\nProbabilidades de medición del estado 'q1':")
                            print(repositorio.medir_estado("q1"))

                            # Crear un operador cuántico (puerta Hadamard)
                            hadamard = OperadorCuantico("H", [[1/np.sqrt(2), 1/np.sqrt(2)], [1/np.sqrt(2), -1/np.sqrt(2)]])

                            # Aplicar el operador al estado 'q2'
                            repositorio.aplicar_operador("q2", hadamard, nuevo_id="q2_H")

                            # Listar estados después de aplicar el operador
                            print("\nEstados en el repositorio después de aplicar Hadamard a 'q2':")
                            for estado in repositorio.listar_estados():
                                print(estado)

                            # Guardar los estados en un archivo JSON
                            repositorio.guardar("estados.json")
                            print("\nEstados guardados en 'estados.json'.")

                            # Cargar estados desde un archivo JSON
                            nuevo_repositorio = RepositorioDeEstados()
                            nuevo_repositorio.cargar("estados.json")
                            print("\nEstados cargados desde 'estados.json':")
                            for estado in nuevo_repositorio.listar_estados():
                                print(estado)