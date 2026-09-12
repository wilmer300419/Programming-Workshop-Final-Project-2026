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
# MIDDLEWARE DE LOGGING
# ============================================================

@app.middleware("http")
async def logging_middleware(
    request: Request,
    call_next
):
    """
    Middleware encargado de registrar las solicitudes
    y medir el tiempo de respuesta.

    IMPORTANTE:

    Las métricas NO se almacenan en memoria.

    El archivo app.log es la fuente de verdad.

    El middleware únicamente registra las solicitudes
    en el sistema de logging.

    Metrics posteriormente lee:

        app.log
        app.log.1
        app.log.2
        app.log.3

    y calcula las métricas.
    """

    # ========================================================
    # EXCLUIR /metrics
    # ========================================================

    # No registramos /metrics para evitar que la consulta
    # de las métricas se contabilice a sí misma.
    if request.url.path == "/metrics":

        return await call_next(request)


    # ========================================================
    # INICIO DEL TIEMPO
    # ========================================================

    # Guarda el momento exacto en el que comienza
    # el procesamiento de la solicitud.
    start_time = time.perf_counter()


    # ========================================================
    # REGISTRO DE LA SOLICITUD
    # ========================================================

    # Registra que se recibió una nueva solicitud.
    logger.info(
        f"REQUEST "
        f"{request.method} "
        f"{request.url.path} "
        f"- Petición recibida"
    )


    try:

        # ====================================================
        # EJECUTAR SOLICITUD
        # ====================================================

        # Ejecuta la ruta correspondiente.

        # Ejemplos:
        #
        # GET /products/
        # POST /products/
        # DELETE /products/1
        #
        response = await call_next(request)


        # ====================================================
        # CALCULAR TIEMPO
        # ====================================================

        # Calcula cuánto tiempo tardó la solicitud.

        # perf_counter() devuelve segundos,
        # por eso multiplicamos por 1000 para obtener
        # milisegundos.
        response_time = (
            time.perf_counter() - start_time
        ) * 1000


        # ====================================================
        # REGISTRO DE SOLICITUD EXITOSA
        # ====================================================

        if response.status_code < 400:

            logger.info(
                f"SUCCESS "
                f"{request.method} "
                f"{request.url.path} "
                f"- HTTP {response.status_code} "
                f"- Tiempo: "
                f"{response_time:.2f} ms"
            )


        # ====================================================
        # REGISTRO DE SOLICITUD CON ERROR
        # ====================================================

        else:

            logger.error(
                f"ERROR "
                f"{request.method} "
                f"{request.url.path} "
                f"- HTTP {response.status_code} "
                f"- Tiempo: "
                f"{response_time:.2f} ms"
            )


        # ====================================================
        # DEVOLVER RESPUESTA
        # ====================================================

        return response


    except Exception as exc:

        # ====================================================
        # CALCULAR TIEMPO DEL ERROR
        # ====================================================

        response_time = (
            time.perf_counter() - start_time
        ) * 1000


        # ====================================================
        # REGISTRAR ERROR 500
        # ====================================================

        # Las métricas NO se actualizan manualmente.
        #
        # Metrics leerá este registro desde app.log
        # y contará el HTTP 500 automáticamente.

        logger.exception(
            f"ERROR "
            f"{request.method} "
            f"{request.url.path} "
            f"- HTTP 500 "
            f"- Tiempo: "
            f"{response_time:.2f} ms "
            f"- Error: {str(exc)}"
        )


        # ====================================================
        # RESPUESTA HTTP 500
        # ====================================================

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
    Maneja los errores de validación generados
    por FastAPI y Pydantic.

    Ejemplos:

    - Falta un campo obligatorio.
    - Se envía texto en lugar de un número.
    - El precio no cumple las restricciones.
    - El stock es inválido.

    Los errores de validación generan HTTP 422.

    IMPORTANTE:

    No actualizamos las métricas manualmente.

    El middleware recibe posteriormente la respuesta
    HTTP 422 y la registra en app.log.
    """

    # ========================================================
    # REGISTRO DEL ERROR DE VALIDACIÓN
    # ========================================================

    # Registramos únicamente información adicional
    # sobre el error de validación.
    #
    # NO colocamos aquí:
    #
    # "HTTP 422"
    #
    # porque el middleware será quien registre la respuesta
    # HTTP 422 con el tiempo real.
    logger.error(
        f"VALIDATION_ERROR "
        f"{request.method} "
        f"{request.url.path} "
        f"- Información de la solicitud inválida: "
        f"{exc.errors()}"
    )


    # ========================================================
    # RESPUESTA DE VALIDACIÓN
    # ========================================================

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
#
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

    El middleware se encarga automáticamente
    de registrar esta solicitud en app.log
    y calcular su tiempo real de respuesta.
    """

    # No registramos manualmente esta solicitud.
    #
    # El middleware genera:
    #
    # SUCCESS GET / - HTTP 200 - Tiempo: X.XX ms

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

    Las métricas son calculadas directamente
    leyendo los archivos de logs.

    Archivos considerados:

        app.log
        app.log.1
        app.log.2
        app.log.3

    /metrics no se registra para evitar
    que se contabilice a sí mismo.
    """

    # ========================================================
    # OBTENER MÉTRICAS DESDE LOS LOGS
    # ========================================================

    # Metrics lee directamente los archivos:
    #
    # app.log
    # app.log.1
    # app.log.2
    # app.log.3
    #
    # y calcula nuevamente los valores.
    current_metrics = metrics.get_metrics()


    # ========================================================
    # RESPUESTA
    # ========================================================

    return {
        "success": True,
        "message": "Métricas consultadas correctamente",
        "data": current_metrics
    }
