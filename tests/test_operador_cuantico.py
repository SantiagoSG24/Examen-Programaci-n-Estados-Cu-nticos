from test_estado_cuantico import EstadoCuantico
from test_operador_cuantico import OperadorCuantico
import unittest
from typing import List, Dict, Union
import math
import numpy as np
import json

class TestOperadorCuantico(unittest.TestCase):
    def test_aplicar_operador_X(self):
        estado = EstadoCuantico("q0", [1, 0], "computacional")
        opX = OperadorCuantico("X", [[0, 1], [1, 0]])
        nuevo_estado = opX.aplicar(estado)
        self.assertEqual(nuevo_estado.vector.tolist(), [0, 1])

    def test_aplicar_operador_H(self):
        estado = EstadoCuantico("q0", [1, 0], "computacional")
        opH = OperadorCuantico("H", [[1/np.sqrt(2), 1/np.sqrt(2)], [1/np.sqrt(2), -1/np.sqrt(2)]])
        nuevo_estado = opH.aplicar(estado)
        self.assertAlmostEqual(nuevo_estado.vector[0], 1/np.sqrt(2))
        self.assertAlmostEqual(nuevo_estado.vector[1], 1/np.sqrt(2))
