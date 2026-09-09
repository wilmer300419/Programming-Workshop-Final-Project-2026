from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.routes.product_routes import router as product_router
from src.utils.logger import logger


# Crea la instancia principal de la API.
app = FastAPI(
    title="API REST - Gestión de Productos",
    description=(
        "API REST desarrollada con Python y FastAPI "
        "para administrar productos."
    ),
    version="1.0.0"
)


# Middleware para registrar todas las peticiones
@app.middleware("http")
async def logging_middleware(request: Request, call_next):

    # Registrar petición recibida
    logger.info(
        f"REQUEST {request.method} {request.url.path} "
        f"- Petición recibida"
    )

    try:

        # Ejecutar la petición
        response = await call_next(request)

        # Registrar finalización
        if response.status_code < 400:

            logger.info(
                f"SUCCESS {request.method} {request.url.path} "
                f"- Operación finalizada correctamente "
                f"(HTTP {response.status_code})"
            )

        else:

            logger.error(
                f"ERROR {request.method} {request.url.path} "
                f"- Operación finalizada con error "
                f"(HTTP {response.status_code})"
            )

        return response

    except Exception as exc:

        # Registrar errores inesperados
        logger.exception(
            f"ERROR {request.method} {request.url.path} "
            f"- Error inesperado: {str(exc)}"
        )

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Error interno del servidor",
                "data": None
            }
        )


# Registrar errores de validación de FastAPI
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):

    logger.error(
        f"VALIDATION_ERROR {request.method} "
        f"{request.url.path} "
        f"- Información de la solicitud inválida: "
        f"{exc.errors()}"
    )

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Los datos enviados no son válidos",
            "data": exc.errors()
        }
    )


# Registra las rutas relacionadas con los productos.
app.include_router(product_router)


# Define la respuesta de la ruta principal de la API.
@app.get("/")
def root():

    logger.info(
        "SUCCESS GET / - Consulta de estado de la API"
    )

    return {
        "success": True,
        "message": "API de productos funcionando correctamente"
    }
