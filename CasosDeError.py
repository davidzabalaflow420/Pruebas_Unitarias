import unittest
import random
import numbers

class Tablero:
    def __init__(self, filas, columnas):
        # Variables para gestionar errores
        self.error_creacion = None
        self.error_colocacion_barcos = None
        self.error_disparo = None

        # Validación de filas y columnas como enteros positivos
        if not isinstance(filas, numbers.Integral) or not isinstance(columnas, numbers.Integral):
            raise ValueError("Las filas y columnas deben ser valores enteros y positivos")
        elif filas <= 0 or columnas <= 0:
            raise ValueError("Las filas y columnas deben ser valores positivos")

        # Inicialización de variables del tablero
        self.disparos_realizados = set()
        self.aciertos = 0
        self.filas = filas
        self.columnas = columnas
        self.matriz = [[' ']*self.columnas for _ in range(self.filas)]
        self.matriz_disparos = []
        self.barcos_hundidos = 0

    def imprimir_separador_horizontal(self):
        # Imprime una línea horizontal para separar las filas del tablero
        print("+---" * self.columnas + "+")

    def imprimir_fila_de_numeros(self):
        # Imprime los números de columna encima del tablero
        print("|   " + "|".join(f" {x+1} " for x in range(self.columnas)) + "|")

    def imprimir_matriz(self, deberia_mostrar_barcos, jugador):
        # Imprime el estado actual del tablero
        print(f"Este es el mar del jugador {jugador}: ")
        letra = "A"
        for y in range(self.filas):
            self.imprimir_separador_horizontal()
            print(f"| {letra} ", end="")
            for x in range(self.columnas):
                celda = self.matriz[y][x]
                valor_real = celda if deberia_mostrar_barcos or celda == ' ' else ' '
                if (x, y) in self.matriz_disparos:
                    valor_real = '-' if celda == ' ' else celda
                    if celda == 'B':
                        self.barcos_hundidos += 1
                print(f"| {valor_real} ", end="")
            letra = chr(ord(letra) + 1)
            print("|")
        self.imprimir_separador_horizontal()
        self.imprimir_fila_de_numeros()

    def colocar_barcos(self, cantidad_barcos):
        # Coloca barcos aleatoriamente en el tablero
        barcos_colocados = 0
        while barcos_colocados < cantidad_barcos:
            x, y = random.randint(0, self.columnas - 1), random.randint(0, self.filas - 1)
            if self.matriz[y][x] == ' ':
                self.matriz[y][x] = 'S'
                barcos_colocados += 1
            else:
                self.error_colocacion_barcos = "Intento de colocar un barco sobre una celda ocupada"
                break

    def disparar(self, x, y):
        # Realiza un disparo en las coordenadas especificadas
        if not isinstance(x, numbers.Integral) or not isinstance(y, numbers.Integral):
            self.error_disparo = "Coordenadas deben ser valores enteros"
            return False

        if x < 0 or x >= self.columnas or y < 0 or y >= self.filas:
            self.error_disparo = "Coordenadas fuera de límites"
            return False

        if (x, y) in self.disparos_realizados:
            self.error_disparo = "Ya se realizó disparo en esta celda"
            return False

        if self.matriz[y][x] == ' ':
            self.matriz[y][x] = '-'
            self.matriz_disparos.append((x, y))
            return False
        elif self.matriz[y][x] == '-':
            return False
        else:
            self.matriz[y][x] = '*'
            self.matriz_disparos.append((x, y))
            self.aciertos += 1
            self.disparos_realizados.add((x, y))
            return True

    def disparar_fuera_de_limites(self, x, y):
        # Verifica si las coordenadas están fuera de límites
        if x < 0 or x >= self.columnas or y < 0 or y >= self.filas:
            self.error_disparo = "Coordenadas fuera de límites"
            return False

class TestTablero(unittest.TestCase):
    def setUp(self):
        # Configura el tablero para las pruebas
        self.tablero = Tablero(5, 5)

    def test_creacion_con_filas_no_enteras(self):
        # Prueba de creación del tablero con filas no enteras
        with self.assertRaises(ValueError):
            Tablero(2.5, 5)

    def test_creacion_con_columnas_no_enteras(self):
        # Prueba de creación del tablero con columnas no enteras
        with self.assertRaises(ValueError):
            Tablero(4, "B")

    def test_colocar_barcos_sobre_celdas_ocupadas(self):
        # Prueba de colocar barcos sobre celdas ya ocupadas
        self.tablero.matriz[2][2] = 'S'
        with self.assertRaises(ValueError, msg="No se levantó ValueError al colocar barcos sobre celdas ocupadas"):
            self.tablero.colocar_barcos(1)

    def test_colocar_barcos_exitosamente(self):
        # Prueba de colocar barcos correctamente
        cantidad_barcos = 3
        try:
            self.tablero.colocar_barcos(cantidad_barcos)
        except ValueError as e:
            self.fail(f"Se generó un ValueError inesperado: {e}")

        barcos_en_tablero = sum(row.count('S') for row in self.tablero.matriz)
        self.assertEqual(barcos_en_tablero, cantidad_barcos)

    def test_disparar_con_coordenadas_invalidas(self):
        # Prueba de disparar con coordenadas fuera de límites
        self.tablero.disparar(6, 2)
        self.assertIsNotNone(self.tablero.error_disparo)

        self.tablero.disparar(2, 6)
        self.assertIsNotNone(self.tablero.error_disparo)

    def test_disparar_con_coordenadas_ya_utilizadas(self):
        # Prueba de disparar en celdas ya utilizadas
        x, y = 2, 2
        self.tablero.disparar(x, y)
        with self.assertRaises(ValueError, msg="No se levantó ValueError al disparar en celda ya utilizada"):
            self.tablero.disparar(x, y)

    def test_disparar_en_celda_ya_utilizada(self):
        # Prueba de disparar en celda ya utilizada
        x, y = 3, 4
        self.tablero.disparar(x, y)
        self.assertIsNotNone(self.tablero.error_disparo)
        self.tablero.disparar(1, 1)
        with self.assertRaises(ValueError, msg="No se levantó ValueError al disparar en celda ya utilizada"):
            self.tablero.disparar(x, y)
            
    def test_disparar_fuera_de_limites(self):
        # Prueba de disparar fuera de límites
        self.tablero.disparar_fuera_de_limites(6, 2)
        self.assertIsNotNone(self.tablero.error_disparo)

        self.tablero.disparar_fuera_de_limites(2, 6)
        self.assertIsNotNone(self.tablero.error_disparo)

if __name__ == '__main__':
    # Ejecución de las pruebas unitarias
    testRunner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=testRunner)
