from estado_cuantico import EstadoCuantico
from typing import List, Dict, Union
class EstadoCuantico:
    def __init__(self, id, vector, base):
        self.id = id
        self.vector = vector
        self.base = base

    def __str__(self):
        return f"ID: {self.id}, Vector: {self.vector}, Base: {self.base}"


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