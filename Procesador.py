from gestor_archivos import GestorArchivos
from conversor_indice import ConversorIndice
from matrices import Matriz
class Procesador:
    def __init__(self, gestor, campos):
        self.gestor = gestor
        self.campos = campos

    def generar_matrices_frecuencia(self):
        nodo_campo = self.campos.primero
        while nodo_campo:
            campo = nodo_campo.dato
            
            #creamos los conversores de indices
            idx_est = ConversorIndice()
            idx_suelo = ConversorIndice()
            idx_cultivo = ConversorIndice()

            #estaciones o filas
            filas = 0
            nodo_est = campo.estaciones.primero
            while nodo_est:
                est = nodo_est.dato
                idx_est.agregar(est.id, filas)
                filas += 1
                nodo_est = nodo_est.siguiente

            #sensores de suelo o columnas
            cols_s = 0
            nodo_ss = campo.sensores_suelo.primero
            while nodo_ss:
                ss = nodo_ss.dato
                idx_suelo.agregar(ss.id, cols_s)
                cols_s += 1
                nodo_ss = nodo_ss.siguiente

            #sensores de cultivo o columnas de f[n,t]
            cols_t = 0
            nodo_sc = campo.sensores_cultivo.primero
            while nodo_sc:
                sc = nodo_sc.dato
                idx_cultivo.agregar(sc.id, cols_t)
                cols_t += 1
                nodo_sc = nodo_sc.siguiente

            #creamos las matrices
            # F[n,s]: filas = estaciones, columnas = sensores de suelo
            F_ns = Matriz(filas, cols_s) if (filas > 0 and cols_s > 0) else None
            # F[n,t]: filas = estaciones, columnas = sensores de cultivo
            F_nt = Matriz(filas, cols_t) if (filas > 0 and cols_t > 0) else None

            #llenamos F[n,s] con frecuencias de sensores de suelo
            if F_ns is not None:
                col = 0
                nodo_ss = campo.sensores_suelo.primero
                while nodo_ss:
                    ss = nodo_ss.dato
                    #recorremos las frecuencias del sensor ss
                    nodo_f = ss.frecuencias.primero
                    while nodo_f:
                        f = nodo_f.dato
                        fila = idx_est.buscar_indice(f.id_estacion) # estacion a fila
                        if fila != -1:
                            F_ns.set(fila, col, f.valor)
                        nodo_f = nodo_f.siguiente
                    col += 1
                    nodo_ss = nodo_ss.siguiente

            # Llenamos F[n,t] con frecuencias de sensores de cultivo
            if F_nt is not None:
                col = 0
                nodo_sc = campo.sensores_cultivo.primero
                while nodo_sc:
                    sc = nodo_sc.dato
                    nodo_f = sc.frecuencias.primero
                    while nodo_f:
                        f = nodo_f.dato
                        fila = idx_est.buscar_indice(f.id_estacion)
                        if fila != -1:
                            F_nt.set(fila, col, f.valor)
                        nodo_f = nodo_f.siguiente
                    col += 1
                    nodo_sc = nodo_sc.siguiente

            #Guardamos en el campo las matrices y conversores
            campo.idx_estaciones = idx_est
            campo.idx_suelo = idx_suelo
            campo.idx_cultivo = idx_cultivo
            campo.F_ns = F_ns
            campo.F_nt = F_nt          
                            
            nodo_campo = nodo_campo.siguiente

    def generar_matrices_patrones(self):
        #Recorremos los campos que ya tienen F_ns y F_nt
        nodo_campo = self.campos.primero
        while nodo_campo:
            campo = nodo_campo.dato

            # si no hay matrices de frecuencia saltamos
            F_ns = getattr(campo, 'F_ns', None)
            F_nt = getattr(campo, 'F_nt', None)

            # funcion para contar filas y columnas
            def dimensiones(matriz):
                #contar filas
                nfilas = 0
                nf = matriz.filas.primero
                while nf:
                    nfilas += 1
                    nf = nf.siguiente
                #contar columnas
                ncols = 0
                nf = matriz.filas.primero
                if nf:
                    nc = nf.dato.celdas.primero
                    while nc:
                        ncols += 1
                        nc = nc.siguiente
                return nfilas, ncols

            #construir Fp para suelo
            if F_ns is not None:
                filas_s, cols_s = dimensiones(F_ns)
                Fp_ns = Matriz(filas_s, cols_s)
                i = 0
                while i < filas_s:
                    j = 0
                    while j < cols_s:
                        val = F_ns.get(i, j)
                        Fp_ns.set(i, j, 1 if val > 0 else 0)  # solo valores positivos
                        j += 1
                    i += 1
                campo.Fp_ns = Fp_ns # guardar matriz de patrones de suelo

            #construir Fp para cultivo
            if F_nt is not None:
                filas_t, cols_t = dimensiones(F_nt)
                Fp_nt = Matriz(filas_t, cols_t)
                i = 0
                while i < filas_t:
                    j = 0
                    while j < cols_t:
                        val = F_nt.get(i, j)
                        Fp_nt.set(i, j, 1 if val > 0 else 0)                        
                        j += 1
                    i += 1
                campo.Fp_nt = Fp_nt # guardar matriz de patrones de cultivo

            nodo_campo = nodo_campo.siguiente            


    def generar_matrices_reducidas(self):
        def dimensiones(matriz):
            # cuenta filas y columnas recorriendo nuestras listas
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

        def filas_iguales(Fp, i, j, ncols):
            # compara fila i con fila j en la matriz de patrones Fp (1/0 por columna)
            c = 0
            while c < ncols:
                if Fp.get(i, c) != Fp.get(j, c):
                    return False
                c += 1
            return True

        # TDA para agrupar indices de filas (estaciones)
        from lista import Lista
        class Grupo:
            def __init__(self):
                self.indices = Lista()   # lista enlazada de indices de filas
            def agregar(self, idx):
                self.indices.insertar(idx)

        # helper para evitar duplicados de indices en los grupos
        def indice_en_grupos(lista_grupos, idx):
            nodo_g = lista_grupos.primero
            while nodo_g:
                nodo_i = nodo_g.dato.indices.primero
                while nodo_i:
                    if nodo_i.dato == idx:
                        return True
                    nodo_i = nodo_i.siguiente
                nodo_g = nodo_g.siguiente
            return False

        # ------------------------------------------------------
        # recorrer cada campo y construir Fr_ns y Fr_nt
        nodo_campo = self.campos.primero
        while nodo_campo:
            campo = nodo_campo.dato

            # matrices de frecuencia (F) y de patrones (Fp)
            F_ns  = getattr(campo, "F_ns", None)   # suelo
            F_nt  = getattr(campo, "F_nt", None)   # cultivo
            Fp_ns = getattr(campo, "Fp_ns", None)  # suelo (patrones)
            Fp_nt = getattr(campo, "Fp_nt", None)  # cultivo (patrones)

            #--------------- suelo: construir Fr_ns ---------------------
            if F_ns is not None and Fp_ns is not None:
                from matrices import Matriz

                nfilas_s, ncols_s = dimensiones(Fp_ns)

                # grupos_s es una lista de objetos Grupo
                grupos_s = Lista()

                # para cada fila i se busca un grupo con el mismo patron #
                # si no existe se crea
                i = 0
                while i < nfilas_s:
                    if indice_en_grupos(grupos_s, i):
                        i += 1
                        continue
                    insertado = False
                    nodo_g = grupos_s.primero
                    while nodo_g and not insertado:
                        # tomar una fila de referencia del grupo (primer indice guardado)
                        ref_node = nodo_g.dato.indices.primero
                        ref = ref_node.dato if ref_node else -1
                        if ref != -1 and filas_iguales(Fp_ns, i, ref, ncols_s):
                            nodo_g.dato.agregar(i)
                            insertado = True
                        nodo_g = nodo_g.siguiente

                    if not insertado:
                        # crear nuevo grupo con i y anexar filas j>i con el mismo patron
                        g = Grupo()
                        g.agregar(i)
                        grupos_s.insertar(g)
                        j = i + 1
                        while j < nfilas_s:
                            if filas_iguales(Fp_ns, i, j, ncols_s) and not indice_en_grupos(grupos_s, j):
                                g.agregar(j)
                            j += 1
                    i += 1

                # contar grupos -> filas de la matriz reducida
                filas_r_s = 0
                aux_g = grupos_s.primero
                while aux_g:
                    filas_r_s += 1
                    aux_g = aux_g.siguiente

                # construir Fr_ns (filas_r_s x ncols_s) sumando filas originales de F_ns por grupo
                Fr_ns = Matriz(filas_r_s, ncols_s)

                fila_r = 0
                aux_g = grupos_s.primero
                while aux_g:
                    c = 0
                    while c < ncols_s:
                        suma = 0
                        nodo_idx = aux_g.dato.indices.primero
                        while nodo_idx:
                            idx_fila = nodo_idx.dato
                            suma += F_ns.get(idx_fila, c)
                            nodo_idx = nodo_idx.siguiente
                        Fr_ns.set(fila_r, c, suma)
                        c += 1
                    fila_r += 1
                    aux_g = aux_g.siguiente

                # guardar matriz reducida y los grupos
                campo.Fr_ns = Fr_ns
                campo.GruposSuelo = grupos_s   

            # ----------------- cultivo: construir Fr_nt ---------------------
            if F_nt is not None and Fp_nt is not None:
                from matrices import Matriz

                nfilas_t, ncols_t = dimensiones(Fp_nt)

                grupos_t = Lista()

                i = 0
                while i < nfilas_t:
                    if indice_en_grupos(grupos_t, i):
                        i += 1
                        continue
                    insertado = False
                    nodo_g = grupos_t.primero
                    while nodo_g and not insertado:
                        ref_node = nodo_g.dato.indices.primero
                        ref = ref_node.dato if ref_node else -1
                        if ref != -1 and filas_iguales(Fp_nt, i, ref, ncols_t):
                            nodo_g.dato.agregar(i)
                            insertado = True
                        nodo_g = nodo_g.siguiente

                    if not insertado:
                        g = Grupo()
                        g.agregar(i)
                        grupos_t.insertar(g)
                        j = i + 1
                        while j < nfilas_t:
                            if filas_iguales(Fp_nt, i, j, ncols_t) and not indice_en_grupos(grupos_t, j):
                                g.agregar(j)
                            j += 1
                    i += 1

                filas_r_t = 0
                aux_g = grupos_t.primero
                while aux_g:
                    filas_r_t += 1
                    aux_g = aux_g.siguiente

                Fr_nt = Matriz(filas_r_t, ncols_t)

                fila_r = 0
                aux_g = grupos_t.primero
                while aux_g:
                    c = 0
                    while c < ncols_t:
                        suma = 0
                        nodo_idx = aux_g.dato.indices.primero
                        while nodo_idx:
                            idx_fila = nodo_idx.dato
                            suma += F_nt.get(idx_fila, c)
                            nodo_idx = nodo_idx.siguiente
                        Fr_nt.set(fila_r, c, suma)
                        c += 1
                    fila_r += 1
                    aux_g = aux_g.siguiente

                campo.Fr_nt = Fr_nt
                campo.GruposCultivo = grupos_t  # opcional

            # siguiente campo
            nodo_campo = nodo_campo.siguiente
