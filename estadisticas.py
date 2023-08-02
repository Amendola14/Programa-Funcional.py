import calendar
import csv
from reportlab.lib.pagesizes import letter
import os
from reportlab.pdfgen import canvas
from matplotlib import pyplot as plt
import matplotlib.backends.backend_pdf as pdf_backend
import matplotlib.pyplot as plt








def generar_grafico_ganancias_auto(patente, ganancias_por_mes):
    meses = list(ganancias_por_mes.keys())
    ganancias = list(ganancias_por_mes.values())

    # Obtener los últimos tres meses
    ultimos_tres_meses = meses[-3:]
    ganancias_ultimos_tres_meses = ganancias[-3:]

    plt.figure(figsize=(8, 6))
    plt.pie(ganancias_ultimos_tres_meses, labels=ultimos_tres_meses, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title(f"Ganancias mensuales para el auto {patente} - Últimos tres meses")
    plt.show()


def calcular_ganancia_por_mes_auto(patente):
    ganancias_por_mes = {}

    with open("viajes.csv", "r", newline="") as archivo:
        lector_csv = csv.reader(archivo)
        next(lector_csv)  

        for fila in lector_csv:
            if len(fila) >= 7 and fila[5] == patente:
                fecha = fila[0]
                monto_viaje = float(fila[4])  # Monto del viaje 
                mes = fecha.split("-")[1]

                ganancia_socio = monto_viaje * 0.7  # La ganancia del socio es el 70% del monto del viaje

                if mes in ganancias_por_mes:
                    ganancias_por_mes[mes] += ganancia_socio
                else:
                    ganancias_por_mes[mes] = ganancia_socio

    return ganancias_por_mes




def calcular_ganancia_por_mes_admin():
    """
    Calcula las ganancias mensuales para el administrador.
    La ganancia es el 30% del precio de cada viaje realizado por cualquier socio.
    Retorna un diccionario con las ganancias acumuladas por mes.
    """
    ganancias_por_mes = {}

    with open("viajes.csv", "r", newline="") as archivo:
        lector_csv = csv.reader(archivo)
        next(lector_csv)  

        for fila in lector_csv:
            if fila[5].replace('.', '', 1).isdigit():  # Verificar que el valor sea numérico
                fecha = fila[0]
                monto_viaje = float(fila[5]) 
                mes = fecha.split("-")[1]

                ganancia_admin = monto_viaje * 0.3

                if mes in ganancias_por_mes:
                    ganancias_por_mes[mes] += ganancia_admin
                else:
                    ganancias_por_mes[mes] = ganancia_admin

    return ganancias_por_mes



def generar_grafico_ganancias_socio(meses, ganancias, ganancia_total):
    plt.figure(figsize=(10, 6))
    plt.plot(meses, ganancias, marker='o')  #  gráfico de línea
    plt.xlabel("Mes")
    plt.ylabel("Ganancias")
    plt.title(f"GANANCIA TOTAL: {ganancia_total:.2f}")  # Mostramos la ganancia total en el título
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    # Guardar la imagen en PDF con el título "GANANCIA TOTAL SOCIO.pdf"
    plt.savefig("PDF/GANANCIA TOTAL SOCIO.pdf")

    # Mostrar el gráfico
    plt.show()


def generar_grafico_ganancias_admin():
    """
    Genera un gráfico de tortas con las ganancias mensuales del administrador.
    """
    ganancias_por_mes = calcular_ganancia_por_mes_admin()
    meses = list(ganancias_por_mes.keys())
    ganancias = list(ganancias_por_mes.values())

    plt.figure(figsize=(8, 8))
    plt.pie(ganancias, labels=meses, autopct='%.1f%%', startangle=140)
    plt.title('Estadísticas de Ganancia por Mes - Administrador')
    plt.axis('equal')
    plt.show()


def calcular_ganancia_por_viaje_admin():
    ganancias_por_mes = {}
    with open("viajes.csv", "r", newline="") as archivo:
        lector_csv = csv.reader(archivo, delimiter=",")
        next(lector_csv) 

        for fila in lector_csv:
            fecha = fila[0]
            precio = float(fila[5]) 
            # Calcular la ganancia del socio (70% del precio del viaje)
            ganancia_socio = precio * 0.7

            # Obtener el mes de la fecha
            mes = fecha.split("-")[1]

            # Agregar la ganancia del socio al mes correspondiente
            if mes in ganancias_por_mes:
                ganancias_por_mes[mes] += ganancia_socio
            else:
                ganancias_por_mes[mes] = ganancia_socio

    return ganancias_por_mes
