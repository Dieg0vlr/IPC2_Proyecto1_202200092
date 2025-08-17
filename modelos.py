from lista import Lista

class Campo:
    def __init__(self, id_, nombre):
        self.id = id_
        self.nombre = nombre
        self.estaciones = Lista()       # sublista de EstacionBase
        self.sensores_suelo = Lista()   # sublista de SensorSuelo
        self.sensores_cultivo = Lista() # sublista de SensorCultivo

class EstacionBase:
    def __init__(self, id_, nombre):
        self.id = id_
        self.nombre = nombre

class Frecuencia:
    def __init__(self, id_estacion, valor):
        self.id_estacion = id_estacion
        self.valor = valor

class SensorSuelo:
    def __init__(self, id_, nombre):
        self.id = id_
        self.nombre = nombre
        self.frecuencias = Lista()  # sublista de Frecuencia

class SensorCultivo:
    def __init__(self, id_, nombre):
        self.id = id_
        self.nombre = nombre
        self.frecuencias = Lista()  # sublista de Frecuencia                