import unittest

class Tablero:
    @staticmethod
    def crear_tablero(filas, columnas):
        if filas < 1 or columnas < 1:
            raise ValueError("Las filas y columnas deben ser positivas")
        return [[0] * columnas for _ in range(filas)]

    @staticmethod
    def colocar_barco(tablero, x, y):
        if x < 0 or x >= len(tablero[0]):
            raise IndexError("La columna está fuera del tablero")
        if y < 0 or y >= len(tablero):
            raise IndexError("La fila está fuera del tablero")
        tablero[y][x] = 1

    @staticmethod
    def disparar(tablero, x, y):
        if x < 0 or x >= len(tablero[0]):
            raise IndexError("Columna inválida para disparar")
        if y < 0 or y >= len(tablero):
            raise IndexError("Fila inválida para disparar")
        if tablero[y][x] == -1:
            raise Exception("No puedes disparar a una celda ya disparada")
        tablero[y][x] = -1

class Pruebas(unittest.TestCase):
    def test_crear_tablero_negativo(self):
        with self.assertRaises(ValueError):
            Tablero.crear_tablero(-3, 5)

    def test_crear_tablero_cero(self):
        with self.assertRaises(ValueError):
            Tablero.crear_tablero(0, 5)

    def test_colocar_barco_columna_negativa(self):
        tablero = Tablero.crear_tablero(5, 5)
        with self.assertRaises(IndexError):
            Tablero.colocar_barco(tablero, -1, 3)

    def test_colocar_barco_fila_negativa(self):
        tablero = Tablero.crear_tablero(5, 5)
        with self.assertRaises(IndexError):
            Tablero.colocar_barco(tablero, 3, -1)

    def test_disparar_columa_negativa(self):
        tablero = Tablero.crear_tablero(5, 5)
        with self.assertRaises(IndexError):
            Tablero.disparar(tablero, -1, 3)

    def test_disparar_celda_disparada(self):
        tablero = Tablero.crear_tablero(5, 5)
        tablero[3][2] = -1
        with self.assertRaises(Exception):
            Tablero.disparar(tablero, 2, 3)

if __name__ == '__main__':
    testRunner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=testRunner)