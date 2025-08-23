from lista import Lista

class ParIdIndice:
    def __init__(self, id_, indice):
        self.id_ = id_
        self.indice = indice

class ConversorIndice:
    def __init__(self):
        self.items = Lista() #lista enlazada de ParIdIndice

    def agregar(self, id_, indice):
        #guarda id, indice en la lista
        self.items.insertar(ParIdIndice(id_, indice))

    def buscar_indice(self, id_):
        #busca el indice asociado a un id
        aux = self.items.primero
        while aux:
            par = aux.dato
            if par.id_ == id_:
                return par.indice
            aux = aux.siguiente
        return -1 #no lo encontro
                