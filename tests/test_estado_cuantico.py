from test_estado_cuantico import EstadoCuantico
import unittest
from typing import List, Dict, Union
import math
import numpy as np
import json


class TestEstadoCuantico(unittest.TestCase):
    def test_creacion_estado_valido(self):
        estado = EstadoCuantico("q0", [1, 0], "computacional")
        self.assertEqual(estado.id, "q0")
        self.assertEqual(estado.vector, [1, 0])
        self.assertEqual(estado.base, "computacional")

    def test_creacion_estado_invalido(self):
        with self.assertRaises(ValueError):
            EstadoCuantico("q0", [], "computacional")
        with self.assertRaises(ValueError):
            EstadoCuantico("q0", [0.5, 0.5], "computacional")  # No normalizado

    def test_medicion_estado(self):
        estado = EstadoCuantico("q0", [1, 0], "computacional")
        probabilidades = estado.medir()
        self.assertAlmostEqual(probabilidades["0"], 1.0)
        self.assertAlmostEqual(probabilidades["1"], 0.0)