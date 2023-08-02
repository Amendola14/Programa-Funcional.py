import csv
import hashlib
import admin
import socio



def validar_login(email, clave):
    clave_cifrada = hashlib.sha256(clave.encode()).hexdigest()
    with open("usuarios.csv", "r") as archivo:
        password=0
        correo=0
        lector_csv = csv.reader(archivo)
        for fila in lector_csv:
            for elemento in fila:
                if elemento == email:
                    correo=1
                elif elemento == clave:
                    password=1
            if correo == 1 and password == 1:
                
                return fila[2]

       




