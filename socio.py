import csv
import datetime
from hashlib import sha256
import hashlib
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from matplotlib import pyplot as plt
import admin
from estadisticas import generar_grafico_ganancias_socio
from geopy.distance import distance
from geopy.distance import geodesic





def cargar_socio():
    """
    Permite cargar los datos de un socio conductor en el sistema.
 

    
    """
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

    # Verificar si la patente ya está asignada a otro socio
    if verificar_patente_existente(patente):
        print("La patente ya está asignada a otro socio. Por favor, ingrese una patente diferente.")
        return

    # Cifrar la clave usando el algoritmo SHA-256
    clave_cifrada = hashlib.sha256(clave.encode("utf-8")).hexdigest()

    # Guardar la información del socio en el archivo "usuarios.csv"
    with open("usuarios.csv", "a+", newline="") as archivo:
        escritor_csv = csv.writer(archivo)
        escritor_csv.writerow([email, clave_cifrada, "socio", nombre, apellido, legajo, patente])

    print("Socio conductor guardado correctamente.")

def verificar_correo_existente(email):
    """
    Verifica si el correo electrónico ya está registrado en el sistema.

    
    """
    with open("usuarios.csv", "r", newline="") as archivo:
        lector_csv = csv.reader(archivo)
        next(lector_csv)  # Ignorar la primera línea de encabezado

        for fila in lector_csv:
            if len(fila) >= 1 and fila[0] == email:
                return True  # El correo electrónico ya está registrado
    return False  # El correo electrónico no está registrado


PATENTES_VALIDAS = ["JKL990", "ABC100", "AC190HYU", "AB912HJK"]

def validar_patente(patente):
    """
    Valida el formato y la existencia de una patente.

    
    """
    p = patente.replace(" ", "").upper()
    if p in PATENTES_VALIDAS:
        return p
    else:
        return None



def verificar_patente_existente(patente):
    """
    Verifica si la patente ya está asignada a otro socio en el sistema.

    
    """
    with open("usuarios.csv", "r", newline="") as archivo:
        lector_csv = csv.reader(archivo, delimiter=',')

        for fila in lector_csv:
            if fila[6] == patente:
                return True  # La patente ya está asignada a otro socio
    return False  



def formatear_patente(patente):
    """
   
    """
    return patente.replace(" ", "").upper()


def mostrar_estadisticas_ganancia_socio():
    patente_auto = input("Ingrese la patente del auto utilizado: ")
    ganancias_por_mes = calcular_ganancia_por_mes_socio(patente_auto)


    if not ganancias_por_mes:
        print("No se encontraron ganancias para la patente especificada.")
        return

    ganancia_total = sum(ganancias_por_mes.values())

    meses_ordenados = sorted(ganancias_por_mes.keys(), key=lambda mes: datetime.strptime(mes, "%B").month)
    ganancias_ordenadas = [ganancias_por_mes[mes] for mes in meses_ordenados]

    generar_grafico_ganancias_socio(meses_ordenados, ganancias_ordenadas, ganancia_total)

def menu_socio():
    while True:
        print("=== Menú Socio ===")
        print("1. Ver Estadísticas de Ganancia")
        print("2. Dar de alta un viaje")
        print("3. Volver al sistema")
        print("0. Salir")
        opcion = int(input("Ingrese una opción: "))

        if opcion == 1:
            mostrar_estadisticas_ganancia_socio()
        elif opcion == 2:
            dar_de_alta_viaje()
        elif opcion == 3:
            admin.volver_menu_sistem()
        elif opcion == 0:
            print("Saliendo del programa.")
            exit()
        else:
            print("Opción inválida. Por favor, intente nuevamente.")


def calcular_ganancia_por_mes_socio(patente_auto):
    ganancias_por_mes = {}
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
                ganancias_por_mes[mes] = ganancias_por_mes.get(mes, 0) + monto_viaje
    return ganancias_por_mes


def guardar_viaje_en_csv(fecha_hora_str, inicio, final, km_recorridos, monto_viaje, patente_auto, socio_dueño,
                         latitud_inicio, longitud_inicio, latitud_final, longitud_final):
    """
    Guarda los datos del viaje en el archivo CSV.

    
    """
    # Convertir la cadena de fecha y hora a un objeto datetime
    fecha_hora_obj = datetime.strptime(fecha_hora_str, "%Y-%m-%d,%H:%M:%S")
    # Obtener la cadena de fecha y hora en el formato deseado sin comas
    fecha_hora_formateada = fecha_hora_obj.strftime("%Y-%m-%d,%H:%M:%S")

    with open("viajes.csv", "a", newline="") as archivo:
        escritor_csv = csv.writer(archivo, delimiter=",")
        escritor_csv.writerow([fecha_hora_formateada, inicio, final, km_recorridos, monto_viaje, patente_auto,
                               socio_dueño, latitud_inicio, longitud_inicio, latitud_final, longitud_final])






def calcular_distancia(latitud_inicio, longitud_inicio, latitud_final, longitud_final):
    inicio = (latitud_inicio, longitud_inicio)
    final = (latitud_final, longitud_final)
    distancia = geodesic(inicio, final).kilometers
    return distancia





def dar_de_alta_viaje():
    fecha_hora_str = input("Ingrese la fecha y hora del viaje (formato: yyyy-mm-dd,hh:mm:ss): ")
    direccion_inicio = input("Ingrese la dirección de inicio del viaje: ")
    direccion_final = input("Ingrese la dirección final del viaje: ")
    patente = input("Ingrese la patente del auto utilizado: ")
    latitud_inicio = float(input("Ingrese la latitud del inicio del viaje: "))
    longitud_inicio = float(input("Ingrese la longitud del inicio del viaje: "))
    latitud_final = float(input("Ingrese la latitud final del viaje: "))
    longitud_final = float(input("Ingrese la longitud final del viaje: "))

    # Calcular la distancia recorrida utilizando GeoPy
    distancia = calcular_distancia(latitud_inicio, longitud_inicio, latitud_final, longitud_final)

    # Calcular el monto del viaje como el 70% de la distancia recorrida
    monto_viaje = distancia * 0.7

    # Obtener la fecha y hora actual para el registro del viaje
    fecha_actual = datetime.now().strftime("%Y-%m-%d,%H:%M:%S")

    # Llamar a la función para guardar el viaje en el archivo CSV
    guardar_viaje_en_csv(fecha_hora_str, direccion_inicio, direccion_final, distancia, monto_viaje, patente, monto_viaje,
                         latitud_inicio, longitud_inicio, latitud_final, longitud_final)

    print("Viaje registrado correctamente.")

def cargar_datos_viaje():
    
    # Verificar formato de fecha y hora
    try:
        fecha_hora_str= datetime.strptime(fecha_hora_str, "%Y-%m-%d,%H:%M:%S")
    except ValueError:
        print("Formato de fecha y hora incorrecto. Intente nuevamente.")
        return

    inicio = input("Ingrese la dirección de inicio del viaje: ")
    final = input("Ingrese la dirección final del viaje: ")
    km_recorridos = float(input("Ingrese la cantidad de kilómetros recorridos: "))

    # Calcular el monto del viaje como el 70% de los kilómetros recorridos
    monto_viaje = km_recorridos * 0.7

    patente_auto = input("Ingrese la patente del auto utilizado: ")


    patente_validada = validar_patente(patente_auto)
    if patente_validada is None:
        print("Patente inválida. Por favor, ingrese una patente válida.")
        return
    
    # Buscar al socio dueño del auto en el archivo "usuarios.csv"
    socio_dueño = None
    with open("usuarios.csv", "r", newline="") as archivo:
        lector_csv = csv.reader(archivo)
        next(lector_csv)   

        for fila in lector_csv:
            if len(fila) >= 7 and fila[6] == patente_auto:
                socio_dueño = fila[0]  # El socio dueño posición 0 (correo electrónico) de la fila
                break

    if socio_dueño is None:
        print("No se encontró al socio dueño del auto. Verifique la patente ingresada.")
        return

    # Calcular la ganancia del socio
    ganancia_socio = monto_viaje

    # Obtener la fecha y hora actual para el registro del viaje
    fecha_actual = datetime.now().strftime("%Y-%m-%d,%H:%M:%S")

    # Guardar los datos del viaje en el archivo "viajes.csv"
    with open("viajes.csv", "a", newline="") as archivo:
        escritor_csv = csv.writer(archivo)
        escritor_csv.writerow([fecha_hora_str, inicio, final, km_recorridos, monto_viaje, patente_auto, socio_dueño, ganancia_socio, fecha_actual])

    print("Viaje registrado correctamente.")