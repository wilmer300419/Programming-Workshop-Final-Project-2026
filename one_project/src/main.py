# Importa FastAPI para crear la aplicación.
# Request permite acceder a la información de cada petición HTTP.
from fastapi import FastAPI, Request

# Importa la excepción que FastAPI utiliza cuando los datos
# enviados por el cliente no cumplen con las validaciones
# definidas en los modelos de Pydantic.
from fastapi.exceptions import RequestValidationError

# JSONResponse permite construir respuestas HTTP
# personalizadas en formato JSON.
from fastapi.responses import JSONResponse


# Importa el router que contiene todas las rutas
# relacionadas con los productos.
#
# Se utiliza "as product_router" para darle un nombre
# más descriptivo dentro de este archivo.
from src.routes.product_routes import router as product_router

# Importa el logger principal de la aplicación.
from src.utils.logger import logger


# ============================================================
# CREACIÓN DE LA APLICACIÓN
# ============================================================

# Crea la instancia principal de FastAPI.
#
# title:
# Nombre que aparecerá en la documentación de Swagger.
#
# description:
# Descripción general de la API.
#
# version:
# Versión actual de la API.
app = FastAPI(
    title="API REST - Gestión de Productos",
    description=(
        "API REST desarrollada con Python y FastAPI "
        "para administrar productos."
    ),
    version="1.0.0"
)


# ============================================================
# MIDDLEWARE DE LOGGING
# ============================================================

# Define un middleware que se ejecutará en cada petición HTTP.
#
# El middleware permite realizar acciones antes y después
# de ejecutar una ruta.
@app.middleware("http")
async def logging_middleware(request: Request, call_next):

    # Registra que se recibió una nueva petición.
    #
    # request.method:
    # Indica el método HTTP utilizado, por ejemplo GET, POST,
    # PUT o DELETE.
    #
    # request.url.path:
    # Indica la ruta solicitada.
    logger.info(
        f"REQUEST {request.method} {request.url.path} "
        f"- Petición recibida"
    )

    try:

        # Ejecuta la petición y permite que FastAPI continúe
        # con el procesamiento normal de la ruta.
        #
        # call_next envía la petición hacia el siguiente
        # middleware o hacia el endpoint correspondiente.
        response = await call_next(request)

        # Comprueba si el código HTTP indica que la operación
        # fue exitosa.
        #
        # Los códigos menores a 400 generalmente representan
        # respuestas exitosas o redirecciones.
        if response.status_code < 400:

            # Registra que la operación terminó correctamente.
            logger.info(
                f"SUCCESS {request.method} {request.url.path} "
                f"- Operación finalizada correctamente "
                f"(HTTP {response.status_code})"
            )

        else:

            # Si el código es 400 o superior, registra
            # la petición como un error.
            logger.error(
                f"ERROR {request.method} {request.url.path} "
                f"- Operación finalizada con error "
                f"(HTTP {response.status_code})"
            )

        # Devuelve la respuesta original al cliente.
        return response

    except Exception as exc:

        # Registra cualquier error inesperado que no haya
        # sido controlado anteriormente.
        #
        # logger.exception() también registra información
        # relacionada con la excepción.
        logger.exception(
            f"ERROR {request.method} {request.url.path} "
            f"- Error inesperado: {str(exc)}"
        )

        # Devuelve una respuesta HTTP 500 indicando
        # que ocurrió un error interno del servidor.
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Error interno del servidor",
                "data": None
            }
        )


# ============================================================
# MANEJO DE ERRORES DE VALIDACIÓN
# ============================================================

# Registra un manejador personalizado para los errores
# de validación generados por FastAPI/Pydantic.
#
# Esto permite reemplazar la respuesta predeterminada
# de FastAPI por una respuesta con el formato de nuestra API.
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):

    # Registra información sobre el error de validación.
    #
    # exc.errors() contiene los detalles de los campos
    # que no cumplieron las reglas de validación.
    logger.error(
        f"VALIDATION_ERROR {request.method} "
        f"{request.url.path} "
        f"- Información de la solicitud inválida: "
        f"{exc.errors()}"
    )

    # Devuelve una respuesta personalizada con HTTP 422.
    #
    # 422 significa que la petición tiene una estructura
    # válida, pero los datos enviados no cumplen
    # las reglas de validación.
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Los datos enviados no son válidos",

            # Devuelve al cliente los detalles de los errores
            # encontrados durante la validación.
            "data": exc.errors()
        }
    )


# ============================================================
# REGISTRO DE LAS RUTAS
# ============================================================

# Registra el router de productos dentro de la aplicación.
#
# Como product_router tiene:
#
# prefix="/products"
#
# las rutas estarán disponibles, por ejemplo, como:
#
# GET    /products/
# GET    /products/{product_id}
# POST   /products/
# PUT    /products/{product_id}
# DELETE /products/{product_id}
app.include_router(product_router)


# ============================================================
# RUTA PRINCIPAL
# ============================================================

# Define una ruta GET para la dirección raíz de la API.
#
# La ruta será:
#
# GET /
@app.get("/")
def root():

    # Registra en los logs que se consultó
    # el estado de la API.
    logger.info(
        "SUCCESS GET / - Consulta de estado de la API"
    )

    # Devuelve una respuesta indicando que la API
    # está funcionando correctamente.
    return {
        "success": True,
        "message": "API de productos funcionando correctamente"
    }