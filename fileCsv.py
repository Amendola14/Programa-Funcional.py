
import os

def mkdir_dir(directory):
    try:
        os.makedirs(directory)
        print(f"Directorio '{directory}' creado exitosamente.")
    except FileExistsError:
        print(f"El directorio '{directory}' ya existe.")

if __name__ == "__main__":
    directory_name = "./data/"
    mkdir_dir(directory_name)
