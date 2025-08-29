from gestor_archivos import GestorArchivos
from conversor_indice import ConversorIndice
from matrices import Matriz
from xml.dom import minidom
from Procesador import Procesador


class Menu:
    def __init__(self):
        self.opcion = 0
        self.gestor = GestorArchivos()  # para llamar mis metodos
        self.campos = None

    def mostrar(self):
        while self.opcion != 6:
            print("--------------------------------")
            print("\n--- Menu Principal ---")
            print("1. Cargar archivo")
            print("2. Procesar archivo")
            print("3. Escribir archivo salida")
            print("4. Mostrar datos del estudiante")
            print("5. Generar grafica")
            print("6. Salida")
            print("--------------------------------")

            try:
                self.opcion = int(input("Seleccione una opcion: "))
            except ValueError:
                print("Por favor, ingrese una opcion valida")
                continue

            if self.opcion == 1:
                self.cargar_archivo()
            elif self.opcion == 2:
                self.procesar_archivo()
            elif self.opcion == 3:
                self.escribir_salida()
            elif self.opcion == 4:
                self.mostrar_estudiante()
            elif self.opcion == 5:
                self.generar_grafica()
            elif self.opcion == 6:
                print("Saliendo del menu...")
            else:
                print("Opcion no valida, por favor intente de nuevo")


    #-------Cargamos todo al menu inicializando las clases--------------
    def cargar_archivo(self):
        ruta = input("Ingrese la ruta del archivo: ").strip()
        nombre = input("Ingrese el nombre del archivo: ").strip()
        self.campos = self.gestor.cargar(ruta, nombre)
        self.procesador = Procesador(self.gestor, self.campos)
    #---------------------------------------------------------------------

    def procesar_archivo(self):
        if self.campos is None:
            print("Primero debe cargar un archivo")
            return
        
        print("\n--- Procesando archivo ---")
        self.procesador.generar_matrices_frecuencia()
        print("Matrices de frecuencia generadas correctamente")
        print("------------------------------------------------")
        self.procesador.generar_matrices_patrones()
        print("Matrices de patrones generadas correctamente")
        print("------------------------------------------------")
        self.procesador.generar_matrices_reducidas()
        print("Matrices reducidas generadas correctamente")
        print("------------------------------------------------")
        print("Procesamiento completado\n")

    #----------------------------------------------------------------------------------------------
    def escribir_salida(self):
        # validar que existan datos
        if self.campos is None:
            print("Primero debe cargar y procesar un archivo")
            return
        
        ruta = input("Ingrese la ruta de destino: ").strip()
        nombre = input("Ingrese el nombre del archivo de salida: ").strip()
        if not nombre.lower().endswith('.xml'):
            nombre += '.xml'

        # armar ruta completa
        ruta = ruta.rstrip('/\\') 
        ruta_completa = (ruta + "/" + nombre) if ruta else nombre

        #---------Crea y llena las matrices------------------------------------------------------

        def dimensiones(matriz):
            nfilas = 0
            nf = matriz.filas.primero
            while nf:
                nfilas += 1
                nf = nf.siguiente
            ncols = 0
            nf = matriz.filas.primero
            if nf:
                nc = nf.dato.celdas.primero
                while nc:
                    ncols += 1
                    nc = nc.siguiente
            return nfilas, ncols
        
        def escribir_matriz(doc, padre, etiqueta, matriz):
            if matriz is None:
                return
            cont = doc.createElement(etiqueta)
            padre.appendChild(cont)

            nfilas, ncols = dimensiones(matriz)
            i = 0
            while i < nfilas:
                fila_el = doc.createElement("fila")
                # construir texto de la fila con espacios alineados
                linea = ""
                for j in range(ncols):
                    val = matriz.get(i, j)
                    if j == 0:
                        linea += str(val).rjust(6)  # Alinea el primer valor a la derecha con 6 espacios
                    else:
                        linea = linea + " " + str(val).rjust(6)  # Alinea los demas valores con 6 espacios de ancho
                fila_el.appendChild(doc.createTextNode(linea))
                cont.appendChild(fila_el)
                i += 1

#-------------------------------- Crear doc XML ----------------------------------------
        try:
            #creamos el xml
            doc = minidom.Document()
            root = doc.createElement("salida")
            doc.appendChild(root)

            # recorrer campos cargados
            nodo_campo = self.campos.primero
            while nodo_campo:
                campo = nodo_campo.dato

                # nodo de cada campo con sus datos basicos
                e_campo = doc.createElement("campo")
                e_campo.setAttribute("id", str(getattr(campo, "id", "")))
                e_campo.setAttribute("nombre", str(getattr(campo, "nombre", "")))
                root.appendChild(e_campo)

                # Guardamos las matrices en el xml
                escribir_matriz(doc, e_campo, "F_ns", getattr(campo, "F_ns", None))
                escribir_matriz(doc, e_campo, "F_nt", getattr(campo, "F_nt", None))
                escribir_matriz(doc, e_campo, "Fp_ns", getattr(campo, "Fp_ns", None))
                escribir_matriz(doc, e_campo, "Fp_nt", getattr(campo, "Fp_nt", None))
                escribir_matriz(doc, e_campo, "Fr_ns", getattr(campo, "Fr_ns", None))
                escribir_matriz(doc, e_campo, "Fr_nt", getattr(campo, "Fr_nt", None))

                nodo_campo = nodo_campo.siguiente
            # Guardamos el xml en archivo
            with open(ruta_completa, 'w', encoding='utf-8') as f:
                xml_str = doc.toprettyxml(indent="  ")
                f.write(xml_str)

            print("Archivo de salida escrito en:", ruta_completa)

        except Exception as e:
            print("Error al escribir el archivo de salida:", e)
 #----------------------------------------------------------------------------------------------              
          

    def mostrar_estudiante(self):
        print("---Datos del Estudiante---")
        print("Nombre: Diego Maldonado")
        print("Carne: 202200092")
        print("Curso: IPC2")
        print("Seccion: B")
        print("4to. Semestre")
        print("https://github.com/Dieg0vlr/IPC2_Proyecto1_202200092.git")


    def generar_grafica(self):
        # valida que existan datos procesados
        if self.campos is None:
            print("Primero debe cargar y procesar un archivo")
            return

        # pedir ruta y nombre del archivo .dot
        ruta = input("Ingrese la ruta destino (carpeta): ").strip()
        nombre = input("Ingrese el nombre del archivo .dot: ").strip()
        if not nombre.lower().endswith(".dot"):
            nombre += ".dot"

        # armar ruta final
        ruta = ruta.rstrip("/\\")
        ruta_completa = (ruta + "/" + nombre) if ruta else nombre

        # Construir un id para DOT sin espacios
        def dot_id(prefijo, id_campo, id_item):
            # evita espacios y simbolos raros
            safe_campo = str (id_campo).replace(" ", "_")
            safe_item = str(id_item).replace(" ", "_")
            return prefijo + "_" + safe_campo + "_" + safe_item       

        # contar filas y columnas de una matriz enlazada
        def dimensiones(matriz):
            nfilas = 0
            nf = matriz.filas.primero
            while nf:
                nfilas += 1
                nf = nf.siguiente
            ncols = 0
            nf = matriz.filas.primero
            if nf:
                nc = nf.dato.celdas.primero
                while nc:
                    ncols += 1
                    nc = nc.siguiente
            return nfilas, ncols

        try:
            # abrimos archivo .dot
            with open(ruta_completa, "w", encoding="utf-8") as f:
                # encabezado del grafo
                f.write("digraph G {\n")
                f.write('  rankdir=LR;\n')
                f.write('  overlap=false;\n')
                f.write('  splines=true;\n')
                f.write('  fontname="Arial";\n')
                f.write('  node [fontname="Arial"];\n')
                f.write('  edge [fontname="Arial"];\n')            

                # Recorrer cada campo para dibujar como un closter
                nodo_campo = self.campos.primero
                while nodo_campo:
                    campo = nodo_campo.dato
                    id_campo = getattr(campo, "id", "")
                    nom_campo = getattr(campo, "nombre", "")

                    # Subgrafo (cluster) para el campo
                    f.write(f'  subgraph cluster_{str(id_campo).replace(" ", "_")} {{\n')
                    f.write('    color="gray70";\n')
                    f.write(f'    label="campo: {nom_campo}";\n')
                    f.write('    labelloc="t";\n')

                    #NODOS DE ESTACIONES
                    f.write('    // estaciones\n')
                    nodo_est = campo.estaciones.primero
                    while nodo_est:
                        est = nodo_est.dato
                        est_id = dot_id("est", id_campo, getattr(est, "id", ""))
                        est_label = str(getattr(est, "id", "")) + "\\n" + str(getattr(est, "nombre", ""))
                        f.write(f'    {est_id} [shape=box, style="rounded,filled", fillcolor="#e8f0fe", label="{est_label}"];\n')
                        nodo_est = nodo_est.siguiente

                    #NODOS DE SENSORES DE SUELO
                    f.write('    // sensores de suelo\n')
                    nodo_ss = campo.sensores_suelo.primero
                    while nodo_ss:
                        ss = nodo_ss.dato
                        ss_id = dot_id("ss", id_campo, getattr(ss, "id", ""))
                        ss_label = "SUELO\\n" + str(getattr(ss, "id", "")) + "\\n" + str(getattr(ss, "nombre", ""))
                        f.write(f'    {ss_id} [shape=ellipse, style="filled", fillcolor="#e6ffed", label="{ss_label}"];\n')
                        nodo_ss = nodo_ss.siguiente

                    # NODOS DE SENSORES DE CULTIVOS
                    f.write('    // sensores de cultivo\n')
                    nodo_sc = campo.sensores_cultivo.primero
                    while nodo_sc:
                        sc = nodo_sc.dato
                        sc_id = dot_id("sc", id_campo, getattr(sc, "id", ""))
                        sc_label = "CULTIVO\\n" + str(getattr(sc, "id", "")) + "\\n" + str(getattr(sc, "nombre", ""))
                        f.write(f'    {sc_id} [shape=ellipse, style="filled", fillcolor="#fff4e6", label="{sc_label}"];\n')
                        nodo_sc = nodo_sc.siguiente

                    #aristas F_ns -> sensor de suelo
                    F_ns = getattr(campo, "F_ns", None)
                    if F_ns is not None:
                        f.write('    // aristas F[n,s] (frecuencia suelo)\n')
                        nfilas_s, ncols_s = dimensiones(F_ns)        

                        # necesitamos mapear indices de fila (estaciones) y columna (sensores suelo)
                        # recorremos estaciones para hacer una lista virtual por posicion 
                        # caminamos de nuevo cuando necesitemos id textual

                        i = 0
                        while i < nfilas_s:
                            # Obtener el nodo de estacion en la posicion i
                            pos = 0
                            nodo_est = campo.estaciones.primero
                            while nodo_est and pos < i:
                                nodo_est = nodo_est.siguiente
                                pos += 1
                            est = nodo_est.dato if nodo_est else None
                            est_id = dot_id("est", id_campo, getattr(est, "id", ""))

                            j = 0
                            while j < ncols_s:
                                # Obtener el nodo del sensor de suelo en la posicion j
                                posc = 0
                                nodo_ss = campo.sensores_suelo.primero
                                while nodo_ss and posc < j:
                                    nodo_ss = nodo_ss.siguiente
                                    posc += 1
                                ss = nodo_ss.dato if nodo_ss else None
                                ss_id = dot_id("ss", id_campo, getattr(ss, "id", "")) if ss else None

                                val = F_ns.get(i, j)
                                if est_id and ss_id and val > 0:
                                    f.write(f'    {est_id} -> {ss_id} [label="{val}", color="#2e7d32"];\n')
                                j += 1
                                # Fin while columnas
                            i += 1
                            #fin while filas         

                    # Aristas F_nt: estacion -> sensor de cultivo
                    F_nt = getattr(campo, "F_nt", None)
                    if F_nt is not None:
                        f.write('    // aristas F[n,t] (frecuencia cultivo)\n')
                        nfilas_t, ncols_t = dimensiones(F_nt)

                        i = 0
                        while i < nfilas_t:
                            # Estacion en posicion i
                            pos = 0
                            nodo_est = campo.estaciones.primero
                            while nodo_est and pos < i:
                                nodo_est = nodo_est.siguiente
                                pos += 1
                            est = nodo_est.dato if nodo_est else None
                            est_id = dot_id("est", id_campo, getattr(est, "id", "")) if est else None

                            j = 0
                            while j < ncols_t:
                                # Sensor de cultivo en posicion j
                                posc = 0
                                nodo_sc = campo.sensores_cultivo.primero
                                while nodo_sc and posc < j:
                                    nodo_sc = nodo_sc.siguiente
                                    posc += 1
                                sc = nodo_sc.dato if nodo_sc else None  
                                sc_id = dot_id("sc", id_campo, getattr(sc, "id", "")) if sc else None

                                val = F_nt.get(i, j)
                                if est_id and sc_id and val > 0:
                                    f.write(f'    {est_id} -> {sc_id} [label="{val}", color="#c62828"];\n')
                                j += 1
                            i += 1

                    # cerrar cluster del campo
                    f.write('  }\n')

                    nodo_campo = nodo_campo.siguiente
                
                # fin del grafo
                f.write("}\n")

            print("Archivo DOT generado en: ", ruta_completa)              

        except Exception as e:
            print("Error al generar la grafica:", e)



                                                            