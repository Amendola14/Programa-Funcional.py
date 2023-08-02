import csv
from hashlib import sha256
import login
import admin
import socio
#"2023-07-27,10:00:00",ABC100,

#admin@hotmail.com1234*,socio1@gmail.com,otraclave1234*#


titulo = "MENU DE INICIO DE SESION"

def main():
    print(titulo)
    print("_" * len(titulo))
    while True:
        email = input("Ingrese su email: ")
        clave = sha256(input("Ingrese su clave: ").encode("UTF-8")).hexdigest()
        perfil = login.validar_login(email, clave)
        if perfil is None:
            print("Credenciales incorrectas. Por favor, intente nuevamente.")    
        elif perfil == "socio":
            socio.menu_socio()
        elif perfil == "admin":
            admin.menu_administrador()        
if __name__ == "__main__":
    main()