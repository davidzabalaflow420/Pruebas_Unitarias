import unittest
import random
import numbers

class Tablero:
    # Declaración e inicialización de variables
    def __init__(self, filas, columnas):
        if not isinstance(filas, numbers.Integral) or not isinstance(columnas, numbers.Integral):
            raise ValueError("Las filas y columnas deben ser valores enteros y positivos")
        if filas <= 0 or columnas <= 0:
            raise ValueError("Las filas y columnas deben ser valores positivos")
        self.disparos_realizados = set()
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
            else:
                raise ValueError("Intento de colocar un barco sobre una celda ocupada")
        
            if barcos_colocados >= cantidad_barcos:
                break

    def disparar(self, x, y):
        if not isinstance(x, numbers.Integral) or not isinstance(y, numbers.Integral):
            raise ValueError("Coordenadas deben ser valores enteros")
      
        # Método para realizar un disparo en la posición (x, y)
        if x < 0 or x >= self.columnas or y < 0 or y >= self.filas:
            raise ValueError("Coordenadas fuera de límites")
        
        if (x, y) in self.disparos_realizados:
            raise ValueError("Ya se realizó disparo en esta celda")
     
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
        
class TestTablero(unittest.TestCase):
    def setUp(self):
        # Se ejecuta antes de cada prueba
        self.tablero = Tablero(5, 5)  # Crear un tablero de 5x5

    def test_creacion_con_filas_no_enteras(self):
        # Prueba de creación con filas no enteras
        with self.assertRaises(ValueError):
            Tablero(2.5, 5)

    def test_creacion_con_columnas_no_enteras(self):
        # Prueba de creación con columnas no enteras
        with self.assertRaises(ValueError):
            Tablero(4, "B")

    def test_colocar_barcos_sobre_celdas_ocupadas(self):
        # Prueba de colocar barcos sobre celdas ya ocupadas
        self.tablero.matriz[2][2] = 'S'  # Ocupar una celda
        with self.assertRaises(ValueError, msg="No se levantó ValueError al colocar barcos sobre celdas ocupadas"):
            try:
                self.tablero.colocar_barcos(1)  # Intentar colocar un barco en la celda ocupada
            except ValueError as e:
                self.assertEqual(str(e), "Intento de colocar un barco sobre una celda ocupada")


    def test_colocar_barcos_exitosamente(self):
        # Prueba de colocar barcos en el tablero
        cantidad_barcos = 3
        self.tablero.colocar_barcos(cantidad_barcos)

        # Verificar que la cantidad de barcos colocados sea la esperada
        barcos_en_tablero = sum(row.count('S') for row in self.tablero.matriz)
        self.assertEqual(barcos_en_tablero, cantidad_barcos)


    def test_disparar_con_coordenadas_invalidas(self):
        # Prueba de disparar con coordenadas fuera de los límites
        with self.assertRaises(ValueError):
            self.tablero.disparar(6, 2)  # Columna fuera de los límites

        with self.assertRaises(ValueError):
            self.tablero.disparar(2, 6)  # Fila fuera de los límites

    def test_disparar_con_coordenadas_ya_utilizadas(self):
        # Prueba de disparar en una celda ya utilizada
        x, y = 2, 2
        self.tablero.disparar(x, y)  # Primer disparo
        with self.assertRaises(ValueError, msg="No se levantó ValueError al disparar en celda ya utilizada"):
            try:
                self.tablero.disparar(x, y)  # Segundo disparo en la misma celda
            except ValueError as e:
                self.assertIn("Ya se realizó disparo en esta celda", str(e))  # Verifica que el mensaje contenga la cadena esperada


    def test_disparar_con_coordenadas_invalidas_tipo(self):
        # Prueba de disparar con coordenadas no enteras
        with self.assertRaises(ValueError):
            self.tablero.disparar(2.5, 3)

        with self.assertRaises(ValueError):
            self.tablero.disparar("A", 2)

if __name__ == '__main__':
    # Ejecución de las pruebas unitarias
    testRunner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=testRunner)
