from typing import List, Union
import math

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