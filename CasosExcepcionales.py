""""
En éste codigo me basé en algo que aprendí, y es que puedo crear bloques donde tenga funciones particulares
para hacer pruebas mas precisas. Lo hice a modo de experimento.
"""
import unittest
# Funciones a probar
class Tablero:
# Función que crea un tablero con la cantidad de filas y columnas especificadas
    def crear_tablero(filas, columnas):
        # Verifica si las filas y columnas son positivas
        if filas < 1 or columnas < 1:
            raise ValueError("Las filas y columnas deben ser positivas")
        # Inicializa el tablero con ceros
        return [[0] * columnas for _ in range(filas)]

    # Función que coloca un barco en las coordenadas especificadas en el tablero
    def colocar_barco(tablero, x, y):
    # Verifica si la columna está dentro del rango del tablero
        if x < 0 or x >= len(tablero[0]):
            raise IndexError("La columna está fuera del tablero")
        # Verifica si la fila está dentro del rango del tablero
        if y < 0 or y >= len(tablero):
            raise IndexError("La fila está fuera del tablero")
        # Coloca un barco en la posición especificada
        tablero[y][x] = 1

    # Función que realiza un disparo en las coordenadas especificadas en el tablero
    def disparar(tablero, x, y):
        # Verifica si la columna está dentro del rango del tablero
        if x < 0 or x >= len(tablero[0]):
            raise IndexError("Columna inválida para disparar")
        # Verifica si la fila está dentro del rango del tablero
        if y < 0 or y >= len(tablero):
            raise IndexError("Fila inválida para disparar")
        # Verifica si la celda ya ha sido disparada
        if tablero[y][x] == -1:
            raise Exception("No puedes disparar a una celda ya disparada")
        # Marca la celda como disparada
        tablero[y][x] = -1

# Pruebas 
class Pruebas(unittest.TestCase):

    # Prueba para asegurarse de que se lance una excepción con un número de filas negativo
    def test_crear_tablero_negativo(self):
        with self.assertRaises(ValueError):
            crear_tablero(-3, 5)
    
    # Prueba para asegurarse de que se lance una excepción con cero filas
    def test_crear_tablero_cero(self):
        with self.assertRaises(ValueError):
            crear_tablero(0, 5)

    # Prueba para asegurarse de que se lance una excepción con una columna negativa
    def test_colocar_barco_columna_negativa(self):
        tablero = crear_tablero(5, 5)
        with self.assertRaises(IndexError):
            colocar_barco(tablero, -1, 3)
    
    # Prueba para asegurarse de que se lance una excepción con una fila negativa
    def test_colocar_barco_fila_negativa(self):
        tablero = crear_tablero(5, 5)
        with self.assertRaises(IndexError):
            colocar_barco(tablero, 3, -1)

    # Prueba para asegurarse de que se lance una excepción con una columna negativa al disparar
    def test_disparar_columa_negativa(self):
        tablero = crear_tablero(5, 5)
        with self.assertRaises(IndexError):
            disparar(tablero, -1, 3)

    # Prueba para asegurarse de que se lance una excepción al disparar a una celda ya disparada
    def test_disparar_celda_disparada(self):
        tablero = crear_tablero(5, 5)
        tablero[3][2] = -1
        with self.assertRaises(Exception):
            disparar(tablero, 2, 3)

if __name__ == '__main__':
    # Ejecución de las pruebas unitarias
    testRunner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=testRunner)
