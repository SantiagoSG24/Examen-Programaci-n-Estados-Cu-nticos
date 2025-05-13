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