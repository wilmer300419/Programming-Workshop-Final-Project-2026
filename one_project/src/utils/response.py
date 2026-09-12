# Importa Any desde typing.
# Any permite indicar que una variable puede contener
# cualquier tipo de dato: string, entero, lista, diccionario, etc.
from typing import Any


# ============================================================
# RESPUESTA EXITOSA
# ============================================================

# Función utilizada para construir respuestas exitosas
# de la API.
#
# message:
# Contiene un mensaje descriptivo sobre el resultado
# de la operación.
#
# data:
# Contiene los datos que se desean devolver.
# Su valor por defecto es None.
def success_response(
    message: str,
    data: Any = None
):

    # Retorna un diccionario con una estructura
    # estándar para las respuestas exitosas.
    return {

        # Indica que la operación fue exitosa.
        "success": True,

        # Mensaje descriptivo de la operación.
        "message": message,

        # Información obtenida o generada por la operación.
        "data": data
    }


# ============================================================
# RESPUESTA DE ERROR
# ============================================================

# Función utilizada para construir respuestas
# cuando ocurre algún error.
#
# message:
# Contiene la descripción del error.
#
# data:
# Permite enviar información adicional relacionada
# con el error. Por defecto es None.
def error_response(
    message: str,
    data: Any = None
):

    # Retorna un diccionario con una estructura
    # estándar para las respuestas de error.
    return {

        # Indica que la operación NO fue exitosa.
        "success": False,

        # Mensaje que explica el error ocurrido.
        "message": message,

        # Información adicional relacionada con el error.
        "data": data
    }