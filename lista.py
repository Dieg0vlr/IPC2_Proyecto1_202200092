class Nodo:
    def __init__(self, dato=None):
        self.dato = dato
        self.siguiente = None
        self.sublista = None #Esto es para listas anidadas

class Lista:
    def __init__(self):
        self.primero = None

    def esta_vacia(self):
        return self.primero is None

    def insertar(self, dato):
        nuevo = Nodo(dato)
        if self.primero is None:
            self.primero = nuevo
        else:
            aux = self.primero
            while aux.siguiente:
                aux = aux.siguiente
            aux.siguiente = nuevo
        return nuevo #regresamos el nodo por si quiero usar sublistas
