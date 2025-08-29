from xml.dom import minidom
from lista import Lista
from modelos import Campo, EstacionBase, SensorSuelo, SensorCultivo, Frecuencia


class GestorArchivos:
    
    def cargar(self, ruta, nombre_archivo):
        ruta_completa = ruta.rstrip("/\\") + "/" + nombre_archivo

        try:
            dom = minidom.parse(ruta_completa)
        except FileNotFoundError:
            print(f"Error: no se encontro el archivo {ruta_completa}")
            return Lista()   # devolvemos lista vacia 
        except Exception as e:
            print(f"Error al abrir el archivo: {e}")
            return Lista()   
        
        lista_campos = Lista() # LISTA DE CAMPOS AGRICOLAS

        raices = dom.getElementsByTagName("camposAgricolas")
        if not raices:
            print("No se encontro etiqueta <camposAgricolas> en el XML")
            return lista_campos
        
        #recorre cada nodo (campo)
        campos = raices[0].getElementsByTagName("campo")
        for campo_node in campos:
            id_campo = campo_node.getAttribute("id")
            nombre_campo = campo_node.getAttribute("nombre")
            print(f"-- Cargando {nombre_campo}")

            #Insertamos el campo en la lista principal
            nodo_campo = lista_campos.insertar(Campo(id_campo, nombre_campo))

            #Estaciones base
            estaciones_base_nodes = campo_node.getElementsByTagName("estacionesBase")
            if estaciones_base_nodes:
                estaciones_nodes = estaciones_base_nodes[0].getElementsByTagName("estacion")
                for e in estaciones_nodes:
                    id_e = e.getAttribute("id")
                    nom_e = e.getAttribute("nombre")
                    nodo_campo.dato.estaciones.insertar(EstacionBase(id_e, nom_e))
                    print(f"   -- Creando estacion base {id_e}")

            #Sensores de suelo
            sensores_suelo_nodes = campo_node.getElementsByTagName("sensoresSuelo")
            if sensores_suelo_nodes:
                sensores_s_nodes = sensores_suelo_nodes[0].getElementsByTagName("sensorS")
                for s in sensores_s_nodes:
                    id_s = s.getAttribute("id")
                    nom_s = s.getAttribute("nombre")
                    nodo_sensor = nodo_campo.dato.sensores_suelo.insertar(SensorSuelo(id_s, nom_s))
                    print(f"   -- Creando sensor de suelo {id_s}")

                    # recorre las frecuencias de este sensor de suelo
                    frecs = s.getElementsByTagName("frecuencia")
                    for f in frecs:
                        id_est = f.getAttribute("idEstacion")
                        val = f.firstChild.data.strip() if f.firstChild else "0"
                        try:
                            valor = int(val)
                        except:
                            valor = 0
                        nodo_sensor.dato.frecuencias.insertar(Frecuencia(id_est, valor))   

            #sensores de cultivo
            sensores_cultivo_nodes = campo_node.getElementsByTagName("sensoresCultivo")
            if sensores_cultivo_nodes:
                sensores_t_nodes = sensores_cultivo_nodes[0].getElementsByTagName("sensorT")
                for t in sensores_t_nodes:
                    id_t = t.getAttribute("id")
                    nom_t = t.getAttribute("nombre")
                    nodo_sensor = nodo_campo.dato.sensores_cultivo.insertar(SensorCultivo(id_t, nom_t))    
                    print(f"   Creando sensor de cultivo {id_t}")     

                    frecs = t.getElementsByTagName("frecuencia")   
                    for f in frecs:
                        id_est = f.getAttribute("idEstacion")
                        val = f.firstChild.data.strip() if f.firstChild else "0"
                        try:
                            valor = int(val)
                        except:
                            valor = 0
                        nodo_sensor.dato.frecuencias.insertar(Frecuencia(id_est, valor))

        print("Archivo cargado correctamente") # listas anidadas
        print("--------------------------------")
        return lista_campos                    

        
