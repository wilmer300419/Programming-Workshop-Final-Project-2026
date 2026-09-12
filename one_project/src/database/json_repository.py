import json
import os


# Obtiene la ruta absoluta de la carpeta donde se encuentra este archivo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Construye la ruta completa del archivo products.json
FILE_PATH = os.path.join(BASE_DIR, "products.json")


def read_products():
    """
    Lee los productos almacenados en el archivo products.json.

    Returns:
        list: Lista de productos. Si el archivo no existe,
              devuelve una lista vacía.
    """

    # Verifica si el archivo products.json existe
    if not os.path.exists(FILE_PATH):
        # Si no existe, retorna una lista vacía
        return []

    # Abre el archivo en modo lectura utilizando codificación UTF-8
    with open(FILE_PATH, "r", encoding="utf-8") as file:

        # Convierte el contenido JSON del archivo en una estructura
        # de datos de Python y la retorna
        return json.load(file)


def write_products(products):
    """
    Guarda la lista de productos en el archivo products.json.

    Args:
        products (list): Lista de productos que se desea almacenar.
    """

    # Abre el archivo en modo escritura.
    # Si no existe, Python lo crea.
    # Si ya existe, reemplaza su contenido.
    with open(FILE_PATH, "w", encoding="utf-8") as file:

        # Convierte la lista de productos a formato JSON
        # y la guarda en el archivo.
        json.dump(
            products,
            file,

            # Agrega una indentación de 4 espacios para
            # que el archivo JSON sea más fácil de leer.
            indent=4,

            # Permite guardar correctamente caracteres especiales
            # como tildes y la letra ñ.
            ensure_ascii=False
        )