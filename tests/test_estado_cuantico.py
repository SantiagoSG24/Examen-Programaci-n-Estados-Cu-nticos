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