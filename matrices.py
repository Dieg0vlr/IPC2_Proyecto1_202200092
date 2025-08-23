from lista import Lista

class Celda:
    def __init__(self, valor=0):
        self.valor = valor

class Fila:
    def __init__(self):
        self.celdas = Lista() #lista de celdas

class Matriz:
    def __init__(self, filas, columnas):
        self.filas = Lista()  # Lista de fila
        #creamos filas
        i = 0
        while i < filas:
            nodo_fila = self.filas.insertar(Fila())
            #creamos columnas
            j = 0
            while j < columnas:
                nodo_fila.dato.celdas.insertar(Celda(0))
                j+= 1
            i += 1

    def _nodo_en_posicion(self, lista, index):
        #Nos devolvera el nodo en la posicion index recorriendo mi lista
        pos = 0
        aux = lista.primero
        while aux is not None and pos < index:
            aux = aux.siguiente
            pos += 1
        return aux

    def set(self, i, j, valor):
        nodo_fila = self._nodo_en_posicion(self.filas, i)
        if nodo_fila is None:
            return
        nodo_celda = self._nodo_en_posicion(nodo_fila.dato.celdas, j)
        if nodo_celda is None:
            return
        nodo_celda.dato.valor = valor

    def get(self, i, j):
        nodo_fila = self._nodo_en_posicion(self.filas, i)
        if nodo_fila is None:
            return 0
        nodo_celda = self._nodo_en_posicion(nodo_fila.dato.celdas, j)
        if nodo_celda is None:
            return 0
        return nodo_celda.dato.valor
            

