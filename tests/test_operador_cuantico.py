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