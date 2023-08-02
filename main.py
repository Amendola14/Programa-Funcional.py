import login
import admin
import socio



def menu_administrador():
    while True:
        print("\n--- Menú Administrador ---")
        print("1. Cargar Socio Conductor")
        print("2. Salir")

        opcion = input("Ingrese el número de opción: ")

        if opcion == "1":
            admin.cargar_socio_conductor()
        elif opcion == "2":
            break
        else:
            print("Opción inválida. Intente nuevamente.")


