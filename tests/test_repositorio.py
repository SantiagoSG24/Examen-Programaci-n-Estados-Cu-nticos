from test_estado_cuantico import EstadoCuantico
import unittest
from typing import List, Dict, Union
import math
import numpy as np
import json
from test_repositorio import RepositorioDeEstados
from test_operador_cuantico import OperadorCuantico


class TestRepositorioDeEstados(unittest.TestCase):
    def setUp(self):
        self.repo = RepositorioDeEstados()

    def test_agregar_y_listar_estados(self):
        self.assertEqual(self.repo.listar_estados(), "No hay estados registrados.")
        self.repo.agregar_estado("q0", [1, 0], "computacional")
        self.repo.agregar_estado("q1", [0, 1], "computacional")
        estados = self.repo.listar_estados()
        self.assertEqual(len(estados), 2)
        self.assertIn("q0", estados[0])
        self.assertIn("q1", estados[1])

    def test_agregar_estado_duplicado(self):
        self.repo.agregar_estado("q0", [1, 0], "computacional")
        mensaje = self.repo.agregar_estado("q0", [0, 1], "computacional")
        self.assertEqual(mensaje, "Error: ya existe un estado con identificador 'q0'.")

    def test_obtener_y_eliminar_estado(self):
        self.repo.agregar_estado("q0", [1, 0], "computacional")
        estado = self.repo.obtener_estado("q0")
        self.assertEqual(estado.id, "q0")
        mensaje = self.repo.eliminar_estado("q0")
        self.assertEqual(mensaje, "Estado 'q0' eliminado correctamente.")
        mensaje = self.repo.obtener_estado("q0")
        self.assertEqual(mensaje, "Error: no existe un estado con identificador 'q0'.")

    def test_aplicar_operador_a_estado(self):
        self.repo.agregar_estado("q0", [1, 0], "computacional")
        opX = OperadorCuantico("X", [[0, 1], [1, 0]])
        mensaje = self.repo.aplicar_operador("q0", opX, "q0_X")
        self.assertEqual(mensaje, "Estado 'q0_X' agregado correctamente.")
        nuevo_estado = self.repo.obtener_estado("q0_X")
        self.assertEqual(nuevo_estado.vector.tolist(), [0, 1])

    def test_guardar_y_cargar_estados(self):
        with tempfile.NamedTemporaryFile(delete=True) as temp_file:
            self.repo.agregar_estado("q0", [1, 0], "computacional")
            self.repo.guardar(temp_file.name)
            self.repo.eliminar_estado("q0")
            self.repo.cargar(temp_file.name)
            estado = self.repo.obtener_estado("q0")
            self.assertEqual(estado.id, "q0")
            self.assertEqual(estado.vector, [1, 0])
