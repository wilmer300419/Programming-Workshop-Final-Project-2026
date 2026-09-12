# Permite medir el tiempo de ejecución
# de cada solicitud.
import time

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.routes.product_routes import router as product_router
from src.utils.logger import logger
from src.utils.metrics import metrics


# ============================================================
# CONFIGURACIÓN PRINCIPAL DE LA APLICACIÓN
# ============================================================

# Crea la aplicación FastAPI.
app = FastAPI(
    title="API REST - Gestión de Productos",
    description=(
        "API REST desarrollada con Python y FastAPI "
        "para administrar productos."
    ),
    version="1.0.0"
)


# ============================================================
# MIDDLEWARE DE LOGGING Y MÉTRICAS
# ============================================================

@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    """
    Middleware que se ejecuta automáticamente
    en cada solicitud HTTP.

    Sus responsabilidades principales son:

    1. Registrar la solicitud en los logs.
    2. Medir el tiempo de respuesta.
    3. Registrar el código HTTP obtenido.
    4. Actualizar las métricas de la aplicación.
    5. Capturar errores internos inesperados.
    """

    # Guarda el momento exacto en el que comienza
    # el procesamiento de la solicitud.
    start_time = time.perf_counter()

    # Registra en el archivo de logs que se recibió
    # una nueva solicitud.
    logger.info(
        f"REQUEST {request.method} {request.url.path} "
        f"- Petición recibida"
    )

    try:

        # Ejecuta la ruta correspondiente.
        #
        # Por ejemplo:
        # GET /products/
        # POST /products/
        # DELETE /products/1
        response = await call_next(request)

        # Calcula cuánto tiempo tardó la solicitud.
        #
        # perf_counter() devuelve el tiempo en segundos,
        # por eso se multiplica por 1000 para convertirlo
        # a milisegundos.
        response_time = (
            time.perf_counter() - start_time
        ) * 1000

        # Registra automáticamente la solicitud
        # dentro del sistema de métricas.
        metrics.register_request(
            response.status_code,
            response_time
        )

        # Si el código HTTP es menor a 400,
        # la solicitud se considera exitosa.
        if response.status_code < 400:

            logger.info(
                f"SUCCESS {request.method} {request.url.path} "
                f"- Operación finalizada correctamente "
                f"(HTTP {response.status_code}) "
                f"- Tiempo: {response_time:.2f} ms"
            )

        else:

            # Si el código es 400 o superior,
            # se registra como error.
            logger.error(
                f"ERROR {request.method} {request.url.path} "
                f"- Operación finalizada con error "
                f"(HTTP {response.status_code}) "
                f"- Tiempo: {response_time:.2f} ms"
            )

        # Devuelve la respuesta al cliente.
        return response

    except Exception as exc:

        # Si ocurre un error inesperado,
        # también se calcula cuánto tardó la solicitud.
        response_time = (
            time.perf_counter() - start_time
        ) * 1000

        # Registra el error como un HTTP 500
        # dentro de las métricas.
        metrics.register_request(
            500,
            response_time
        )

        # logger.exception() registra el mensaje
        # junto con la información del error.
        logger.exception(
            f"ERROR {request.method} {request.url.path} "
            f"- Error inesperado: {str(exc)} "
            f"- Tiempo: {response_time:.2f} ms"
        )

        # Devuelve una respuesta estándar de error interno.
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

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    """
    Maneja los errores de validación generados por FastAPI
    y Pydantic.

    Ejemplos:

    - Falta un campo obligatorio.
    - Se envía texto en lugar de un número.
    - El precio es menor o igual a cero.
    - El stock es negativo.
    """

    # Registra que ocurrió un error de validación.
    metrics.register_validation_error()

    # Guarda el error en el sistema de logs.
    logger.error(
        f"VALIDATION_ERROR {request.method} "
        f"{request.url.path} "
        f"- Información de la solicitud inválida: "
        f"{exc.errors()}"
    )

    # Devuelve una respuesta personalizada
    # para los errores de validación.
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Los datos enviados no son válidos",
            "data": exc.errors()
        }
    )


# ============================================================
# REGISTRO DE RUTAS
# ============================================================

# Incluye todas las rutas relacionadas
# con los productos.
#
# El router ya tiene el prefijo:
# /products
app.include_router(product_router)


# ============================================================
# ENDPOINT PRINCIPAL
# ============================================================

@app.get("/")
def root():
    """
    Endpoint utilizado para comprobar que
    la API está funcionando correctamente.
    """

    # Registra la consulta en los logs.
    logger.info(
        "SUCCESS GET / - Consulta de estado de la API"
    )

    # Devuelve el estado de la aplicación.
    return {
        "success": True,
        "message": "API de productos funcionando correctamente"
    }


# ============================================================
# ENDPOINT DE MÉTRICAS
# ============================================================

@app.get("/metrics")
def get_metrics():
    """
    Endpoint encargado de consultar las métricas
    actuales de la aplicación.

    Ejemplo:

    GET /metrics
    """

    # Obtiene las métricas calculadas
    # por la clase Metrics.
    current_metrics = metrics.get_metrics()

    # Devuelve las métricas utilizando
    # la misma estructura estándar de respuesta
    # utilizada por la aplicación.
    return {
        "success": True,
        "message": "Métricas consultadas correctamente",
        "data": current_metrics
    }