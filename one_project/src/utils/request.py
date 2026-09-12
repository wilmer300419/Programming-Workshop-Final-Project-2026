# Importa Request desde FastAPI.
# Request permite acceder a la información de una petición HTTP,
# incluyendo headers, parámetros, cuerpo (body), etc.
from fastapi import Request


# Función asíncrona encargada de obtener el contenido JSON
# enviado dentro del cuerpo de una petición HTTP.
async def get_request_json(request: Request):

    # request.json() lee el cuerpo de la petición y convierte
    # el contenido JSON en una estructura de datos de Python.
    #
    # Se utiliza "await" porque la lectura del cuerpo de la
    # petición es una operación asíncrona.
    return await request.json()