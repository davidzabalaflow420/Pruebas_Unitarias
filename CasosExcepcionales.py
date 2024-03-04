import unittest

class Tablero:
    # Método estático para crear un tablero con las dimensiones dadas
    @staticmethod
    def crear_tablero(filas, columnas):
        # Verificar que las dimensiones sean positivas
        if filas < 1 or columnas < 1:
            raise ValueError("Las filas y columnas deben ser positivas")
        # Inicializar el tablero con celdas vacías (valor 0)
        return [[0] * columnas for _ in range(filas)]

    # Método estático para colocar un barco en las coordenadas dadas del tablero
    @staticmethod
    def colocar_barco(tablero, x, y):
        # Verificar que las coordenadas estén dentro de los límites del tablero
        if x < 0 or x >= len(tablero[0]):
            raise IndexError("La columna está fuera del tablero")
        if y < 0 or y >= len(tablero):
            raise IndexError("La fila está fuera del tablero")
        # Colocar el barco en la posición dada (cambiar el valor a 1)
        tablero[y][x] = 1

    # Método estático para realizar un disparo en las coordenadas dadas del tablero
    @staticmethod
    def disparar(tablero, x, y):
        # Verificar que las coordenadas estén dentro de los límites del tablero
        if x < 0 or x >= len(tablero[0]):
            raise IndexError("Columna inválida para disparar")
        if y < 0 or y >= len(tablero):
            raise IndexError("Fila inválida para disparar")
        # Verificar si la celda ya ha sido disparada
        if tablero[y][x] == -1:
            raise Exception("No puedes disparar a una celda ya disparada")
        # Marcar la celda como disparada (cambiar el valor a -1)
        tablero[y][x] = -1

class Pruebas(unittest.TestCase):
    # Prueba para verificar el manejo de valores negativos al crear el tablero
    def test_crear_tablero_negativo(self):
        with self.assertRaises(ValueError):
            Tablero.crear_tablero(-3, 5)

    # Prueba para verificar el manejo de filas con valor cero al crear el tablero
    def test_crear_tablero_cero(self):
        with self.assertRaises(ValueError):
            Tablero.crear_tablero(0, 5)

    # Prueba para verificar el manejo de columna negativa al colocar un barco
    def test_colocar_barco_columna_negativa(self):
        tablero = Tablero.crear_tablero(5, 5)
        with self.assertRaises(IndexError):
            Tablero.colocar_barco(tablero, -1, 3)

    # Prueba para verificar el manejo de fila negativa al colocar un barco
    def test_colocar_barco_fila_negativa(self):
        tablero = Tablero.crear_tablero(5, 5)
        with self.assertRaises(IndexError):
            Tablero.colocar_barco(tablero, 3, -1)

    # Prueba para verificar el manejo de columna negativa al realizar un disparo
    def test_disparar_columa_negativa(self):
        tablero = Tablero.crear_tablero(5, 5)
        with self.assertRaises(IndexError):
            Tablero.disparar(tablero, -1, 3)

    # Prueba para verificar el manejo de disparo a una celda ya disparada
    def test_disparar_celda_disparada(self):
        tablero = Tablero.crear_tablero(5, 5)
        tablero[3][2] = -1
        with self.assertRaises(Exception):
            Tablero.disparar(tablero, 2, 3)

if __name__ == '__main__':
    # Configuración y ejecución de las pruebas
    testRunner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=testRunner)
