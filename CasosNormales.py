import unittest
import random

class Tablero:
    # Declaración e inicialización de variables
    def __init__(self, filas, columnas):
        self.aciertos = 0
        self.filas = filas
        self.columnas = columnas
        self.matriz = [[' ']*self.columnas for _ in range(self.filas)]
        self.matriz_disparos = []
        self.barcos_hundidos = 0

    def imprimir_separador_horizontal(self):
        # Método para imprimir una línea separadora horizontal en la matriz
        print("+---" * self.columnas + "+")

    def imprimir_fila_de_numeros(self):
        # Método para imprimir la fila de números sobre la matriz
        print("|   " + "|".join(f" {x+1} " for x in range(self.columnas)) + "|")

    def imprimir_matriz(self, deberia_mostrar_barcos, jugador):
        # Método para imprimir la matriz del tablero
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
        # Método para colocar barcos aleatorios en el tablero
        barcos_colocados = 0
        while True:
            x, y = random.randint(0, self.columnas-1), random.randint(0, self.filas-1)
            if self.matriz[y][x] == ' ':
                self.matriz[y][x] = 'S'
                barcos_colocados += 1
            if barcos_colocados >= cantidad_barcos:
                break

    def disparar(self, x, y):
        # Método para realizar un disparo en la posición (x, y)
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
            return True

# Pruebas unitarias

class TestTablero(unittest.TestCase):
    def setUp(self):
        # Se ejecuta antes de cada prueba
        self.tablero = Tablero(5, 5)  # Crear un tablero de 5x5

    def test_creacion_tablero(self):
        # Prueba de la creación del tablero
        self.assertEqual(self.tablero.filas, 5)
        self.assertEqual(self.tablero.columnas, 5)
        self.assertEqual(len(self.tablero.matriz), 5)
        self.assertEqual(len(self.tablero.matriz[0]), 5)

    def test_inicializacion_matriz(self):
        # Prueba de la inicialización de la matriz
        for fila in self.tablero.matriz:
            for celda in fila:
                self.assertEqual(celda, ' ')

    def test_colocar_barcos(self):
        # Prueba de la colocación de barcos en el tablero
        self.tablero.colocar_barcos(3)
        self.assertEqual(self.tablero.barcos_hundidos, 0)

    def test_colocar_barcos_cantidad_correcta(self):
        # Prueba de la colocación de la cantidad correcta de barcos
        cantidad_barcos = 3
        self.tablero.colocar_barcos(cantidad_barcos)
        self.assertEqual(sum(row.count('S') for row in self.tablero.matriz), cantidad_barcos)

    def test_disparar_fallado(self):
        # Prueba de un disparo fallido
        x, y = 2, 2
        self.assertFalse(self.tablero.matriz[y][x] == 'S')
        self.assertFalse(self.tablero.matriz[y][x] == '*')
        self.assertFalse(self.tablero.matriz[y][x] == '-')
        self.tablero.disparar(x, y)
        self.assertEqual(self.tablero.matriz[y][x], '-')

    def test_disparar_acertado(self):
        # Prueba de un disparo acertado
        x, y = 3, 3
        self.assertFalse(self.tablero.matriz[y][x] == '*')
        self.assertFalse(self.tablero.matriz[y][x] == '-')
        self.tablero.matriz[y][x] = 'S'
        self.tablero.disparar(x, y)
        self.assertEqual(self.tablero.matriz[y][x], '*')

if __name__ == '__main__':
    # Ejecución de las pruebas unitarias
    testRunner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=testRunner)
