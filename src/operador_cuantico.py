from typing import List
import math
from estado_cuantico import EstadoCuantico

class OperadorCuantico:
    def __init__(self, nombre: str, matriz: List[List[complex]]):
        """
        Inicializa un operador cuántico con un nombre y su matriz de transformación.
        
        Args:
            nombre: Nombre identificativo del operador (ej. "X", "H")
            matriz: Matriz de transformación (lista de listas de números complejos)
        """
        self.nombre = nombre
        self.matriz = matriz
        
        # Verificar que la matriz sea cuadrada
        n = len(matriz)
        for fila in matriz:
            if len(fila) != n:
                raise ValueError("La matriz del operador debe ser cuadrada")
    
    def aplicar(self, estado: EstadoCuantico) -> EstadoCuantico:
        """
        Aplica el operador a un estado cuántico, devolviendo un nuevo estado.
        
        Args:
            estado: Estado cuántico a transformar
            
        Returns:
            Nuevo estado cuántico resultante de la aplicación del operador
        """
        # Verificar que las dimensiones coincidan
        if len(estado.vector) != len(self.matriz):
            raise ValueError(f"Dimensiones incompatibles: operador {len(self.matriz)}x{len(self.matriz)}, estado {len(estado.vector)}")
            
        # Multiplicación matriz-vector
        nuevo_vector = []
        for fila in self.matriz:
            componente = sum(f * v for f, v in zip(fila, estado.vector))
            nuevo_vector.append(componente)
            
        # Crear nuevo estado con el mismo ID + sufijo del operador
        nuevo_id = f"{estado.id}_{self.nombre}"
        return EstadoCuantico(nuevo_id, nuevo_vector, estado.base)
    
    def __str__(self) -> str:
        return f"Operador {self.nombre} (matriz {len(self.matriz)}x{len(self.matriz)})"
    
    def __repr__(self) -> str:
        return f"OperadorCuantico(nombre={self.nombre!r}, matriz={self.matriz!r})"

# Operadores predefinidos
def crear_operador_x() -> OperadorCuantico:
    """Crea la puerta X (NOT cuántico)"""
    return OperadorCuantico("X", [
        [0, 1],
        [1, 0]
    ])

def crear_operador_h() -> OperadorCuantico:
    """Crea la puerta Hadamard"""
    h = 1/math.sqrt(2)
    return OperadorCuantico("H", [
        [h, h],
        [h, -h]
    ])

def crear_operador_z() -> OperadorCuantico:
    """Crea la puerta Z"""
    return OperadorCuantico("Z", [
        [1, 0],
        [0, -1]
    ])