import unittest
import tempfile
import os
from src.repositorio import RepositorioDeEstados
from src.estado_cuantico import EstadoCuantico
from src.operador_cuantico import crear_operador_x

class TestRepositorioDeEstados(unittest.TestCase):
    def setUp(self):
        self.repo = RepositorioDeEstados()
        self.estado0 = EstadoCuantico("q0", [1, 0])
        self.estado1 = EstadoCuantico("q1", [0, 1])
        self.op_x = crear_operador_x()
    
    def test_agregar_y_listar(self):
        self.repo.agregar_estado("q0", [1, 0])
        self.repo.agregar_estado("q1", [0, 1])
        
        estados = self.repo.listar_estados()
        self.assertEqual(len(estados), 2)
        self.assertIn("q0", estados[0])
        self.assertIn("q1", estados[1])
    
    def test_agregar_duplicado(self):
        self.repo.agregar_estado("q0", [1, 0])
        with self.assertRaises(ValueError):
            self.repo.agregar_estado("q0", [0, 1])
    
    def test_obtener_estado(self):
        self.repo.agregar_estado("q0", [1, 0])
        estado = self.repo.obtener_estado("q0")
        self.assertEqual(estado.id, "q0")
        self.assertIsNone(self.repo.obtener_estado("no_existe"))
    
    def test_aplicar_operador(self):
        self.repo.agregar_estado("q0", [1, 0])
        nuevo_estado = self.repo.aplicar_operador("q0", self.op_x)
        
        self.assertEqual(nuevo_estado.id, "q0_X")
        self.assertAlmostEqual(nuevo_estado.vector[0], 0)
        self.assertAlmostEqual(nuevo_estado.vector[1], 1)
        
        # Verificar que hay dos estados ahora (original y transformado)
        self.assertEqual(len(self.repo.listar_estados()), 2)
    
    def test_medir_estado(self):
        self.repo.agregar_estado("q0", [1, 0])
        probs = self.repo.medir_estado("q0")
        self.assertAlmostEqual(probs["0"], 1.0)
        self.assertAlmostEqual(probs["1"], 0.0)
    
    def test_persistencia(self):
        # Crear un archivo temporal para pruebas
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as tmp:
            temp_filename = tmp.name
        
        try:
            # Agregar estados y guardar
            self.repo.agregar_estado("q0", [1, 0])
            self.repo.agregar_estado("q1", [0, 1])
            self.repo.guardar(temp_filename)
            
            # Crear nuevo repositorio y cargar
            nuevo_repo = RepositorioDeEstados()
            nuevo_repo.cargar(temp_filename)
            
            # Verificar que los estados se cargaron correctamente
            estados = nuevo_repo.listar_estados()
            self.assertEqual(len(estados), 2)
            self.assertIn("q0", estados[0])
            self.assertIn("q1", estados[1])
            
        finally:
            # Limpiar: eliminar el archivo temporal
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)

if __name__ == "__main__":
    unittest.main()

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


                import unittest
from src.estado_cuantico import EstadoCuantico

class TestEstadoCuantico(unittest.TestCase):
    def test_creacion_estado(self):
        estado = EstadoCuantico("q0", [1, 0], "computacional")
        self.assertEqual(estado.id, "q0")
        self.assertEqual(estado.vector, [1, 0])
        self.assertEqual(estado.base, "computacional")
        
    def test_medicion_estado_base(self):
        estado = EstadoCuantico("q0", [1, 0])
        probs = estado.medir()
        self.assertAlmostEqual(probs["0"], 1.0)
        self.assertAlmostEqual(probs["1"], 0.0)
        
        estado = EstadoCuantico("q1", [0, 1])
        probs = estado.medir()
        self.assertAlmostEqual(probs["0"], 0.0)
        self.assertAlmostEqual(probs["1"], 1.0)
    
    def test_medicion_superposicion(self):
        estado = EstadoCuantico("q+", [0.70710678, 0.70710678])  # 1/sqrt(2) ≈ 0.70710678
        probs = estado.medir()
        self.assertAlmostEqual(probs["0"], 0.5, places=5)
        self.assertAlmostEqual(probs["1"], 0.5, places=5)
    
    def test_normalizacion(self):
        with self.assertRaises(ValueError):
            EstadoCuantico("q_err", [1, 1])  # No normalizado
            
        EstadoCuantico("q_ok", [0.6, 0.8])  # 0.6² + 0.8² = 1
    
    def test_str_repr(self):
        estado = EstadoCuantico("q0", [1, 0])
        self.assertIn("q0", str(estado))
        self.assertIn("vector", str(estado))
        self.assertIn("EstadoCuantico", repr(estado))

if __name__ == "__main__":
    unittest.main()

    import unittest
from src.operador_cuantico import OperadorCuantico, crear_operador_x, crear_operador_h
from src.estado_cuantico import EstadoCuantico

class TestOperadorCuantico(unittest.TestCase):
    def test_operador_x(self):
        op_x = crear_operador_x()
        self.assertEqual(op_x.nombre, "X")
        
        # Aplicar X a |0> debe dar |1>
        estado0 = EstadoCuantico("q0", [1, 0])
        estado1 = op_x.aplicar(estado0)
        self.assertAlmostEqual(estado1.vector[0], 0)
        self.assertAlmostEqual(estado1.vector[1], 1)
        
        # Aplicar X a |1> debe dar |0>
        estado1_orig = EstadoCuantico("q1", [0, 1])
        estado0_result = op_x.aplicar(estado1_orig)
        self.assertAlmostEqual(estado0_result.vector[0], 1)
        self.assertAlmostEqual(estado0_result.vector[1], 0)
    
    def test_operador_h(self):
        op_h = crear_operador_h()
        self.assertEqual(op_h.nombre, "H")
        
        # Aplicar H a |0> debe dar |+>
        estado0 = EstadoCuantico("q0", [1, 0])
        estado_plus = op_h.aplicar(estado0)
        h = 1/2**0.5  # 1/sqrt(2)
        self.assertAlmostEqual(estado_plus.vector[0], h)
        self.assertAlmostEqual(estado_plus.vector[1], h)
        
        # Aplicar H dos veces debe devolver al estado original
        estado_original = op_h.aplicar(estado_plus)
        self.assertAlmostEqual(estado_original.vector[0], 1, places=5)
        self.assertAlmostEqual(estado_original.vector[1], 0, places=5)
    
    def test_dimension_incompatible(self):
        op = OperadorCuantico("test", [[1, 0], [0, 1]])
        estado = EstadoCuantico("q_err", [1, 0, 0])  # 3 componentes
        with self.assertRaises(ValueError):
            op.aplicar(estado)

if __name__ == "__main__":
    unittest.main()




    import unittest
import tempfile
import os
from src.repositorio import RepositorioDeEstados
from src.estado_cuantico import EstadoCuantico
from src.operador_cuantico import crear_operador_x

class TestRepositorioDeEstados(unittest.TestCase):
    def setUp(self):
        self.repo = RepositorioDeEstados()
        self.estado0 = EstadoCuantico("q0", [1, 0])
        self.estado1 = EstadoCuantico("q1", [0, 1])
        self.op_x = crear_operador_x()
    
    def test_agregar_y_listar(self):
        self.repo.agregar_estado("q0", [1, 0])
        self.repo.agregar_estado("q1", [0, 1])
        
        estados = self.repo.listar_estados()
        self.assertEqual(len(estados), 2)
        self.assertIn("q0", estados[0])
        self.assertIn("q1", estados[1])
    
    def test_agregar_duplicado(self):
        self.repo.agregar_estado("q0", [1, 0])
        with self.assertRaises(ValueError):
            self.repo.agregar_estado("q0", [0, 1])
    
    def test_obtener_estado(self):
        self.repo.agregar_estado("q0", [1, 0])
        estado = self.repo.obtener_estado("q0")
        self.assertEqual(estado.id, "q0")
        self.assertIsNone(self.repo.obtener_estado("no_existe"))
    
    def test_aplicar_operador(self):
        self.repo.agregar_estado("q0", [1, 0])
        nuevo_estado = self.repo.aplicar_operador("q0", self.op_x)
        
        self.assertEqual(nuevo_estado.id, "q0_X")
        self.assertAlmostEqual(nuevo_estado.vector[0], 0)
        self.assertAlmostEqual(nuevo_estado.vector[1], 1)
        
        # Verificar que hay dos estados ahora (original y transformado)
        self.assertEqual(len(self.repo.listar_estados()), 2)
    
    def test_medir_estado(self):
        self.repo.agregar_estado("q0", [1, 0])
        probs = self.repo.medir_estado("q0")
        self.assertAlmostEqual(probs["0"], 1.0)
        self.assertAlmostEqual(probs["1"], 0.0)
    
    def test_persistencia(self):
        # Crear un archivo temporal para pruebas
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as tmp:
            temp_filename = tmp.name
        
        try:
            # Agregar estados y guardar
            self.repo.agregar_estado("q0", [1, 0])
            self.repo.agregar_estado("q1", [0, 1])
            self.repo.guardar(temp_filename)
            
            # Crear nuevo repositorio y cargar
            nuevo_repo = RepositorioDeEstados()
            nuevo_repo.cargar(temp_filename)
            
            # Verificar que los estados se cargaron correctamente
            estados = nuevo_repo.listar_estados()
            self.assertEqual(len(estados), 2)
            self.assertIn("q0", estados[0])
            self.assertIn("q1", estados[1])
            
        finally:
            # Limpiar: eliminar el archivo temporal
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)

if __name__ == "__main__":
    unittest.main()