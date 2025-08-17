from gestor_archivos import GestorArchivos

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



    def cargar_archivo(self):
        ruta = input("Ingrese la ruta del archivo: ").strip()
        nombre = input("Ingrese el nombre del archivo: ").strip()
        self.campos = self.gestor.cargar(ruta, nombre)

    def procesar_archivo(self):
        print("ACA VA UNA FUNCION")

    def escribir_salida(self):
        print("ACA VA UNA FUNCION")

    def mostrar_estudiante(self):
        print("---Datos del Estudiante---")
        print("Nombre: Diego Maldonado")
        print("Carne: 202200092")
        print("Curso: IPC2")
        print("Seccion: B")
        print("4t0. Semestre")
        print("ACA VA EL ENLAZE A MI DOCUMENTACION")
        
        
        


                                                            