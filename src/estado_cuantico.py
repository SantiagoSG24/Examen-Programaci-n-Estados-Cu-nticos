import json
from typing import List, Dict, Union
import math

class EstadoCuantico:
    def __init__(self, id: str, vector: List[complex], base: str = "computacional"):
        """
        Inicializa un estado cuántico con un identificador único, vector de amplitudes y base.
        
        Args:
            id: Identificador único del estado
            vector: Lista de amplitudes complejas que representan el estado
            base: Base en la que está expresado el estado (por defecto "computacional")
        """
        if not vector:
            raise ValueError("El vector de estado no puede estar vacío")
            
        self.id = id
        self.vector = vector
        self.base = base
        
        # Verificar normalización (con cierta tolerancia)
        suma_cuadrados = sum(abs(amp)**2 for amp in self.vector)
        if not math.isclose(suma_cuadrados, 1.0, rel_tol=1e-5):
            raise ValueError(f"El vector no está normalizado (suma de cuadrados = {suma_cuadrados})")

    def medir(self) -> Dict[str, float]:
        """
        Calcula las probabilidades de medición para cada estado base.
        
        Returns:
            Diccionario con las probabilidades de cada resultado de medición.
            Las claves son strings representando los estados base (ej. "0", "1", etc.)
        """
        probabilidades = {}
        for i, amplitud in enumerate(self.vector):
            prob = abs(amplitud)**2
            estado_base = str(i)  # "0", "1", etc.
            probabilidades[estado_base] = prob
            
        return probabilidades
    
    def __str__(self) -> str:
        """
        Representación legible del estado cuántico.
        """
        vector_str = "[" + ", ".join(f"{a.real:.3f}{a.imag:+.3f}j" for a in self.vector) + "]"
        return f"{self.id}: vector={vector_str} en base {self.base}"
    
    def __repr__(self) -> str:
        return f"EstadoCuantico(id={self.id!r}, vector={self.vector!r}, base={self.base!r})"
    
    def to_dict(self) -> Dict[str, Union[str, List[complex]]]:
        """
        Convierte el estado a un diccionario para serialización.
        """
        return {
            "id": self.id,
            "vector": self.vector,
            "base": self.base
        }
    
    @classmethod
    def from_dict(cls, data: Dict [ str, Union[str, List[complex]]]):
        """
        Crea un EstadoCuantico a partir de un diccionario.
        """
        return cls(data["id"], data["vector"], data["base"])
