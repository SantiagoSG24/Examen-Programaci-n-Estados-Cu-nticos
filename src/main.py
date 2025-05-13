import numpy as np

# Crear un array de NumPy
array = np.array([1, 2, 3, 4, 5])

# Operaciones básicas
print("Suma:", np.sum(array))
print("Media:", np.mean(array))
print("Máximo:", np.max(array))
print("Mínimo:", np.min(array))

# Operaciones con matrices
matrix = np.array([[1, 2], [3, 4]])
print("Transpuesta:\n", np.transpose(matrix))
print("Producto punto:\n", np.dot(matrix, matrix))