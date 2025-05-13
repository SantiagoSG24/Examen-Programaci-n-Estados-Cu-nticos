import json
from typing import Dict, List, Optional
from estado_cuantico import EstadoCuantico
from operador_cuantico import OperadorCuantico

class RepositorioDeEstados:
    def __init__(self):
        """Inicializa un repositorio vacío de estados cuánticos."""
        self.estados: Dict[str, EstadoCuantico] = {}
    
    def agregar_estado(self, id: str, vector: List[complex], base: str = "computacional") -> None:
        """
        Agrega un nuevo estado cuántico al repositorio.
        
        Args:
            id: Identificador único del estado
            vector: Vector de amplitudes complejas
            base: Base en la que está expresado el estado
            
        Raises:
            ValueError: Si ya existe un estado con el mismo ID
        """
        if id in self.estados:
            raise ValueError(f"Ya existe un estado con ID '{id}'")
            
        self.estados[id] = EstadoCuantico(id, vector, base)
    
    def obtener_estado(self, id: str) -> Optional[EstadoCuantico]:
        """
        Obtiene un estado cuántico por su ID.
        
        Args:
            id: Identificador del estado a buscar
            
        Returns:
            El estado cuántico si existe, None en caso contrario
        """
        return self.estados.get(id)
    
    def listar_estados(self) -> List[str]:
        """
        Devuelve una lista con las representaciones en string de todos los estados.
        
        Returns:
            Lista de strings descriptivos de cada estado
        """
        return [str(estado) for estado in self.estados.values()]
    
    def aplicar_operador(self, id_estado: str, operador: OperadorCuantico, nuevo_id: str = None) -> EstadoCuantico:
        """
        Aplica un operador cuántico a un estado y guarda el resultado.
        
        Args:
            id_estado: ID del estado a transformar
            operador: Operador cuántico a aplicar
            nuevo_id: ID para el nuevo estado (si None, se genera automáticamente)
            
        Returns:
            El nuevo estado cuántico resultante
            
        Raises:
            ValueError: Si no existe el estado con el ID especificado
        """
        estado = self.obtener_estado(id_estado)
        if estado is None:
            raise ValueError(f"No existe estado con ID '{id_estado}'")
            
        nuevo_estado = operador.aplicar(estado)
        
        if nuevo_id is not None:
            nuevo_estado.id = nuevo_id
        elif f"{estado.id}_{operador.nombre}" in self.estados:
            # Si el ID generado ya existe, añadir un número
            i = 1
            while f"{estado.id}_{operador.nombre}_{i}" in self.estados:
                i += 1
            nuevo_estado.id = f"{estado.id}_{operador.nombre}_{i}"
        
        self.estados[nuevo_estado.id] = nuevo_estado
        return nuevo_estado
    
    def medir_estado(self, id: str) -> Dict[str, float]:
        """
        Mide un estado cuántico y devuelve las probabilidades de cada resultado.
        
        Args:
            id: ID del estado a medir
            
        Returns:
            Diccionario con las probabilidades de cada resultado de medición
            
        Raises:
            ValueError: Si no existe el estado con el ID especificado
        """
        estado = self.obtener_estado(id)
        if estado is None:
            raise ValueError(f"No existe estado con ID '{id}'")
            
        return estado.medir()
    
    def guardar(self, archivo: str) -> None:
        """
        Guarda todos los estados en un archivo JSON.
        
        Args:
            archivo: Ruta del archivo donde guardar los datos
        """
        datos = [estado.to_dict() for estado in self.estados.values()]
        
        # Convertir números complejos a un formato serializable
        def default_encoder(obj):
            if isinstance(obj, complex):
                return {"__complex__": True, "real": obj.real, "imag": obj.imag}
            raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")
        
        with open(archivo, 'w') as f:
            json.dump(datos, f, default=default_encoder, indent=2)
    
    def cargar(self, archivo: str) -> None:
        """
        Carga estados desde un archivo JSON.
        
        Args:
            archivo: Ruta del archivo desde donde cargar los datos
        """
        def object_hook(obj):
            if "__complex__" in obj:
                return complex(obj["real"], obj["imag"])
            return obj
        
        with open(archivo, 'r') as f:
            datos = json.load(f, object_hook=object_hook)
        
        # Limpiar el repositorio antes de cargar
        self.estados.clear()
        
        for dato in datos:
            try:
                estado = EstadoCuantico.from_dict(dato)
                self.estados[estado.id] = estado
            except Exception as e:
                print(f"Error al cargar estado {dato.get('id')}: {e}")