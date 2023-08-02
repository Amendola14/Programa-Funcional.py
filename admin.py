import datetime
import hashlib
import os
from datetime import datetime
import csv
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import sistema
import estadisticas
from socio import formatear_patente













def menu_administrador():
    while True:
        print("=== Menú Administrador ===")
        print("1. Cargar Socio Conductor")
        print("2. Cargar Datos de un Auto")
        print("3. Ver Estadísticas de Ganancia")
        print("4. Volver al sistema")
        print("0. Salir")
        opcion = int(input("Ingrese una opción: "))

        if opcion == 1:
            cargar_socio()
        elif opcion == 2:
            cargar_datos_auto()
        elif opcion == 3:
            mostrar_estadisticas_ganancia_admin()
        elif opcion == 4:
            return
        elif opcion == 0:
            print("Saliendo del programa.")
            exit()
        else:
            print("Opción inválida. Por favor, intente nuevamente.")























def volver_menu_sistem():
    sistema.main()
    exit()


def cargar_datos_auto():
    
    patente = input("Ingrese la patente del auto: ")
    modelo = int(input("Ingrese el año del modelo del auto: "))
    categoria = input("Ingrese la categoría del auto (A/GAMA ALTA o B/GAMA BAJA): ").upper()
    servicio = input("Ingrese el servicio del auto (F/FULL o C/SEMI-COMPLETO): ").upper()
    
    
    if len(patente) != 6:
        print("La patente debe tener exactamente 6 caracteres.")
        return
    
    if verificar_patente_existente(patente):
            print("La patente ya está asignada a otro socio. Por favor, ingrese una patente diferente.")
            return
    
    if modelo < 2004:
        print("No se pueden incluir modelos de autos menores a 2004.")
        return

    if categoria not in ["A", "B"]:
        print("Categoría inválida. Las opciones válidas son A (GAMA ALTA) o B (GAMA BAJA).")
        return

    if servicio not in ["F", "C"]:
        print("Servicio inválido. Las opciones válidas son F (FULL) o C (SEMI-COMPLETO).")
        return

    with open("autos.csv", "+a", newline="") as archivo:
        escritor_csv = csv.writer(archivo)
        escritor_csv.writerow([patente, modelo, categoria, servicio])
    print("Datos del auto guardados correctamente.")













    

def verificar_patente_existente(patente):
    with open("autos.csv", "r", newline="") as archivo:
        lector_csv = csv.reader(archivo, delimiter=',') 

        for fila in lector_csv:
            if fila[0] == patente:
                return True  # La patente ya está asignada a otro socio
    return False  # La patente no está asignada a ningún socio








def validar_patente(_patente):
    p = formatear_patente(_patente)

    if len(p) != 6:
        return -1

    for i in range(3):
        if not p[i].isalpha() or not p[i + 3].isdigit():
            return -1

    return p




def registrar_auto():
    patente = input("Ingrese la patente del auto: ")
    modelo = int(input("Ingrese el año del modelo del auto: "))
    categoria = input("Ingrese la categoría del auto (A/GAMA ALTA o B/GAMA BAJA): ").upper()
    servicio = input("Ingrese el servicio del auto (F/FULL o C/SEMI-COMPLETO): ").upper()

    if modelo < 2004:
        print("No se pueden incluir modelos de autos menores a 2004.")
        return

    if categoria not in ["A", "B"]:
        print("Categoría inválida. Las opciones válidas son A (GAMA ALTA) o B (GAMA BAJA).")
        return

    if servicio not in ["F", "C"]:
        print("Servicio inválido. Las opciones válidas son F (FULL) o C (SEMI-COMPLETO).")
        return

    patente_valida = validar_patente(patente)

    if patente_valida == -1:
        print("La patente ingresada es incorrecta.")
        return

    with open("autos.csv", "a+", newline="") as archivo:
        escritor_csv = csv.writer(archivo)
        escritor_csv.writerow([patente_valida, modelo, categoria, servicio])
        escritor_csv.close()















def cargar_socio():
    nombre = input("Ingrese el nombre del socio: ")
    apellido = input("Ingrese el apellido del socio: ")
    legajo = input("Ingrese el número de legajo del socio: ")
    email = input("Ingrese el email del socio: ")
    clave = input("Ingrese la clave del socio: ")
    
    
# Verificar si el correo electrónico ya está registrado
    if verificar_correo_existente(email):
        print("El correo electrónico ya está registrado. Por favor, ingrese un correo diferente.")
        return

    patente = input("Ingrese la patente del socio conductor: ")

# Verificar si la pemtente  ya está registrado

    if verificar_patente_existente(patente):
        print("La patente ya está asignada a otro socio. Por favor, ingrese una patente diferente.")
        return

    
    clave_cifrada = hashlib.sha256(clave.encode("utf-8")).hexdigest()
    

    with open("usuarios.csv", "a+", newline="") as archivo:
        escritor_csv = csv.writer(archivo)
        escritor_csv.writerow([email, clave_cifrada, "socio", nombre, apellido, legajo, patente])
        
    print("Socio conductor guardado correctamente.")

def verificar_correo_existente(email):
    with open("usuarios.csv", "r", newline="") as archivo:
        lector_csv = csv.reader(archivo)
        next(lector_csv)  

        for fila in lector_csv:
            if len(fila) >= 1 and fila[0] == email:
                return True  # El correo electrónico ya está registrado
    return False  # El correo electrónico no está registrado
















def calcular_ganancia_por_patente(patente_auto):
    ganancias_por_patente = {}
    with open("viajes.csv", newline="") as archivo:
        lector_csv = csv.reader(archivo)
        next(lector_csv)  
        for fila in lector_csv:
            patente = fila[5]
            if patente == patente_auto:
                fecha_hora_str = fila[0]
                fecha_hora = datetime.strptime(fecha_hora_str, "%Y-%m-%d,%H:%M:%S")
                mes = fecha_hora.strftime("%B")
                monto_viaje_str = fila[3]  
                try:
                    monto_viaje = float(monto_viaje_str)
                except ValueError:
                    print(f"El valor de ganancia '{monto_viaje_str}' no es válido en el viaje con patente {patente_auto}.")
                    continue

                ganancias_por_patente[mes] = ganancias_por_patente.get(mes, 0) + monto_viaje

    return ganancias_por_patente



def generar_grafico_ganancias_admin(ganancias_por_patente, ganancia_total_admin, patente_auto):
  
    import matplotlib.pyplot as plt

    meses = list(ganancias_por_patente.keys())
    ganancias = list(ganancias_por_patente.values())

    plt.figure(figsize=(8, 8))
    plt.pie(ganancias, labels=meses, autopct='%1.1f%%', startangle=140)
    plt.title(f"Ganancias por Mes para la Patente: {patente_auto}\nGanancia Total del ADMINISTRADOR: {ganancia_total_admin:.2f}")
    plt.axis('equal')
    archivo_imagen = f"grafico_{patente_auto}.png"
    plt.savefig(f"images/{archivo_imagen}")

    plt.show()


def mostrar_estadisticas_ganancia_por_patente(patente_auto):
    ganancias_por_patente = {}
    with open("viajes.csv", newline="") as archivo:
        lector_csv = csv.reader(archivo)
        next(lector_csv)  
        for fila in lector_csv:
            patente = fila[5]
            if patente == patente_auto:
                fecha_hora_str = fila[0]
                fecha_hora = datetime.strptime(fecha_hora_str, "%Y-%m-%d,%H:%M:%S")
                mes = fecha_hora.strftime("%B")
                monto_viaje = float(fila[3])  
                ganancias_por_patente[mes] = ganancias_por_patente.get(mes, 0) + monto_viaje

    if not ganancias_por_patente:
        print("No se encontraron ganancias para la patente especificada.")
        return

    ganancia_total_conductor = sum(ganancias_por_patente.values())
    ganancia_total_admin = ganancia_total_conductor * 0.3 

    meses_ordenados = sorted(ganancias_por_patente.keys(), key=lambda mes: datetime.strptime(mes, "%B").month)
    ganancias_conductor_ordenadas = [ganancias_por_patente[mes] for mes in meses_ordenados]
    ganancias_admin_ordenadas = [ganancia * 0.3 for ganancia in ganancias_conductor_ordenadas]

    generar_grafico_ganancias_admin(meses_ordenados, ganancias_conductor_ordenadas, ganancia_total_conductor)
    generar_grafico_ganancias_admin(meses_ordenados, ganancias_admin_ordenadas, ganancia_total_admin)



def mostrar_estadisticas_ganancia_admin():
    patente_auto = input("Ingrese la patente del auto utilizado: ")

    ganancias_por_patente = calcular_ganancia_por_patente(patente_auto)

    if not ganancias_por_patente:
        print("No se encontraron ganancias para la patente especificada.")
        return

    ganancia_total_conductor = sum(ganancias_por_patente.values())

    ganancia_total_admin = ganancia_total_conductor * 0.3

    print("Ganancia Total del Conductor:", ganancia_total_conductor)
    print("Ganancia del Administrador (30%):", ganancia_total_admin)

    generar_grafico_ganancias_admin(ganancias_por_patente, ganancia_total_admin, patente_auto)

    # Guardar el gráfico en formato PDF
    guardar_grafico_en_pdf(ganancias_por_patente, patente_auto, ganancia_total_admin)





def generar_grafico_ganancias_torta(ganancias_por_mes_y_viaje):
    labels = []
    sizes = []

    for mes, ganancias_viaje in ganancias_por_mes_y_viaje.items():
        for ganancia_viaje in ganancias_viaje:
            labels.append(f"{mes}: ${ganancia_viaje:.2f}")
            sizes.append(ganancia_viaje)

    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title("Ganancias por Viaje")
    plt.axis('equal')
    plt.show()




    
def guardar_grafico_en_pdf(ganancias_por_patente, patente_auto, ganancia_total_adminmistrador):
    carpeta_pdf = "PDF"
    if not os.path.exists(carpeta_pdf):
        os.makedirs(carpeta_pdf)

    archivo_pdf = os.path.join(carpeta_pdf, f"{patente_auto}_grafico.pdf")

    viajes = list(ganancias_por_patente.keys())
    ganancias = list(ganancias_por_patente.values())

    plt.figure(figsize=(8, 8))
    plt.pie(ganancias, labels=viajes, autopct='%1.1f%%', startangle=140)
    plt.title(f"Distribución de Ganancias por Viaje\nGanancia Total del ADMINISTRADOR: {ganancia_total_adminmistrador:.2f}")
    plt.axis('equal')

    plt.savefig(archivo_pdf)
    plt.close()

    print("El gráfico se ha guardado correctamente en formato PDF.")