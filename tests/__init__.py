from typing import List, Dict, Union
import math
import numpy as np
import json
import json

class EstadoCuantico:
    def __init__(self, id: str, vector: List[Union[complex, float]], base: str):
        if not vector:
            raise ValueError("El vector no puede estar vacío.")
        if not math.isclose(sum(abs(amplitud)**2 for amplitud in vector), 1.0, rel_tol=1e-9):
            raise ValueError("El vector debe estar normalizado (la suma de |componentes|^2 debe ser 1).")
        
        self.id = id
        self.vector = vector
        self.base = base

    def medir(self):
        """Calcula las probabilidades de medir cada estado base."""
        probabilidades = [abs(amplitud)**2 for amplitud in self.vector]
        return {str(i): prob for i, prob in enumerate(probabilidades)}

    def __str__(self):
        return f"{self.id}: vector={self.vector} en base {self.base}"

# Ejemplo de uso:
if __name__ == "__main__":
    # Crear un estado cuántico en superposición igualitaria
    estado = EstadoCuantico("q1", [0.707+0j, 0.707+0j], "computacional")
    print(estado)  # Salida: q1: vector=[(0.707+0j), (0.707+0j)] en base computacional
    print(estado.medir())  # Salida: {'0': 0.5, '1': 0.5}


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





class RepositorioDeEstados:
    def __init__(self):
        self.estados = {}

    def listar_estados(self):
        if not self.estados:
            return "No hay estados registrados."
        return [str(estado) for estado in self.estados.values()]

    def agregar_estado(self, id, vector, base):
        if id in self.estados:
            return f"Error: ya existe un estado con identificador '{id}'."
        self.estados[id] = EstadoCuantico(id, vector, base)
        return f"Estado '{id}' agregado correctamente."

    def obtener_estado(self, id):
        if id not in self.estados:
            return f"Error: no existe un estado con identificador '{id}'."
        return self.estados[id]

    def eliminar_estado(self, id):
        if id not in self.estados:
            return f"Error: no existe un estado con identificador '{id}'."
        del self.estados[id]
        return f"Estado '{id}' eliminado correctamente."


# Pruebas de funcionalidad
if __name__ == "__main__":
    repo = RepositorioDeEstados()
    print(repo.listar_estados())  # Esperado: "No hay estados registrados."

    print(repo.agregar_estado("q0", [1, 0], "computacional"))  # Agregar q0
    print(repo.agregar_estado("q1", [0, 1], "computacional"))  # Agregar q1
    print(repo.listar_estados())  # Mostrar q0 y q1

    print(repo.agregar_estado("q1", [0.5, 0.5], "computacional"))  # Error: duplicado
    print(repo.obtener_estado("q0"))  # Mostrar q0
    print(repo.obtener_estado("q2"))  # Error: no existe q2

    print(repo.eliminar_estado("q1"))  # Eliminar q1
    print(repo.listar_estados())  # Mostrar solo q0

def aplicar_operador(self, id_estado: str, operador: OperadorCuantico, nuevo_id: str = None):
        """
        Aplica un operador cuántico a un estado existente en el repositorio.
        :param id_estado: Identificador del estado cuántico a transformar.
        :param operador: OperadorCuantico a aplicar.
        :param nuevo_id: Identificador del nuevo estado resultante (opcional).
        """
        # Verificar si el estado existe
        estado = self.obtener_estado(id_estado)
        if isinstance(estado, str):  # Si obtener_estado devuelve un mensaje de error
            return f"Error: no se pudo encontrar el estado con id '{id_estado}'."

        # Validar dimensiones del operador y el estado
        if len(estado.vector) != operador.matriz.shape[0]:
            return f"Error: las dimensiones del operador '{operador.nombre}' no coinciden con el estado '{id_estado}'."

        # Aplicar el operador al estado
        nuevo_estado = operador.aplicar(estado)

        # Determinar el identificador del nuevo estado
        if nuevo_id:
            nuevo_estado.id = nuevo_id
        else:
            nuevo_estado.id = f"{id_estado}_{operador.nombre}"

        # Agregar o actualizar el estado en el repositorio
        if nuevo_estado.id in self.estados:
            self.estados[nuevo_estado.id] = nuevo_estado  # Sobrescribir si ya existe
            return f"Estado '{nuevo_estado.id}' actualizado correctamente."
        else:
            self.estados[nuevo_estado.id] = nuevo_estado  # Agregar nuevo estado
            return f"Estado '{nuevo_estado.id}' agregado correctamente."
        


def medir_estado(self, id_estado: str):
        """
        Mide un estado cuántico registrado en el repositorio y obtiene las probabilidades de cada resultado.
        :param id_estado: Identificador del estado cuántico a medir.
        :return: Formato entendible de las probabilidades o mensaje de error si el estado no existe.
        """
        # Buscar el estado en el repositorio
        estado = self.obtener_estado(id_estado)
        if isinstance(estado, str):  # Si obtener_estado devuelve un mensaje de error
            return f"Error: no se pudo encontrar el estado con id '{id_estado}'."

        # Obtener las probabilidades de medición
        probabilidades = estado.medir()

        # Formatear el resultado
        resultado = f"Medición del estado {estado.id} (base {estado.base}):\n"
        for estado_base, probabilidad in probabilidades.items():
            porcentaje = round(probabilidad * 100, 2)
            resultado += f" - Estado base {estado_base}: {porcentaje}%\n"

        return resultado

        def guardar(self, archivo: str):
            """
            Guarda todos los estados en un archivo JSON.
            :param archivo: Nombre del archivo donde se guardarán los estados.
            """
            try:
                with open(archivo, mode='w') as file:
                    lista_estados = []
                    for estado in self.estados.values():
                        lista_estados.append({
                            "id": estado.id,
                            "base": estado.base,
                            "vector": [complex(c).real if c.imag == 0 else str(c) for c in estado.vector]
                        })
                    json.dump(lista_estados, file, indent=4)
                print(f"Estados guardados en {archivo} ({len(self.estados)} estados).")
            except Exception as e:
                print(f"Error al guardar los estados: {e}")

        def cargar(self, archivo: str):
            """
            Carga estados desde un archivo JSON.
            :param archivo: Nombre del archivo desde donde se cargarán los estados.
            """
            try:
                with open(archivo) as file:
                    lista_estados = json.load(file)
                    self.estados.clear()  # Limpiar estados actuales antes de cargar
                    for estado_data in lista_estados:
                        id = estado_data["id"]
                        base = estado_data["base"]
                        vector = [
                            complex(c) if isinstance(c, str) and 'j' in c else float(c)
                            for c in estado_data["vector"]
                        ]
                        self.agregar_estado(id, vector, base)
                print(f"Estados cargados desde {archivo} ({len(self.estados)} estados).")
            except FileNotFoundError:
                print(f"Error: El archivo {archivo} no existe.")
            except Exception as e:
                print(f"Error al cargar los estados: {e}")

