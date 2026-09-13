# Importa el módulo logging de Python, utilizado para
# crear y administrar registros (logs) de la aplicación.
import logging

# Importa os para trabajar con carpetas y rutas del sistema.
import os

# Importa RotatingFileHandler, que permite guardar los logs
# en archivos y crear archivos de respaldo automáticamente
# cuando el archivo alcanza un tamaño determinado.
from logging.handlers import RotatingFileHandler


# ============================================================
# CONFIGURACIÓN DEL DIRECTORIO DE LOGS
# ============================================================

# Define el nombre de la carpeta donde se almacenarán
# los archivos de logs.
LOG_DIR = "logs"

# Crea la carpeta "logs" si todavía no existe.
#
# exist_ok=True evita que se produzca un error si la carpeta
# ya existe.
os.makedirs(LOG_DIR, exist_ok=True)


# ============================================================
# FORMATO DE LOS LOGS
# ============================================================

# Define el formato que tendrán los mensajes registrados.
#
# %(asctime)s -> Fecha y hora del evento.
# %(levelname)s -> Nivel del log (INFO, ERROR, WARNING, etc.).
# %(message)s -> Mensaje que nosotros enviamos al logger.
LOG_FORMAT = (
    "%(asctime)s %(levelname)s "
    "%(message)s"
)


# Define el formato en el que se mostrará la fecha y hora.
#
# Ejemplo:
# 2026-09-12 17:30:45
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


# ============================================================
# CREACIÓN DEL LOGGER
# ============================================================

# Crea o recupera un logger llamado "product_api".
#
# Este será el logger principal utilizado por nuestra
# aplicación de productos.
logger = logging.getLogger("product_api")

# Establece el nivel mínimo de información que será registrado.
#
# INFO permite registrar mensajes de tipo:
# INFO, WARNING, ERROR y CRITICAL.
logger.setLevel(logging.INFO)


# ============================================================
# CONFIGURACIÓN DE LOS HANDLERS
# ============================================================

# Comprueba si el logger ya tiene handlers configurados.
#
# Esto evita agregar los mismos handlers varias veces,
# algo que puede provocar que los mensajes aparezcan
# duplicados en la terminal o en el archivo.
if not logger.handlers:

    # ========================================================
    # HANDLER PARA ARCHIVO
    # ========================================================

    # Crea un handler que almacena los logs en un archivo.
    #
    # RotatingFileHandler permite rotar el archivo cuando
    # alcanza el tamaño máximo configurado.
    file_handler = RotatingFileHandler(

        # Archivo donde se almacenarán los logs.
        "logs/app.log",

        # Tamaño máximo del archivo:
        # 5 * 1024 * 1024 bytes = 5 MB.
        maxBytes=5 * 1024 * 1024,

        # Cantidad de archivos de respaldo que se conservarán.
        #
        # Cuando app.log alcanza 5 MB, se genera un respaldo
        # y se pueden conservar hasta 3 archivos anteriores.
        backupCount=3,

        # Permite almacenar correctamente caracteres
        # especiales como tildes y ñ.
        encoding="utf-8"
    )

    # Establece el nivel mínimo de este handler en INFO.
    file_handler.setLevel(logging.INFO)

    # Define el formato que tendrán los mensajes
    # almacenados en el archivo.
    file_handler.setFormatter(
        logging.Formatter(
            LOG_FORMAT,
            datefmt=DATE_FORMAT
        )
    )


    # ========================================================
    # HANDLER PARA TERMINAL
    # ========================================================

    # Crea un handler para mostrar los logs directamente
    # en la terminal donde se ejecuta la aplicación.
    console_handler = logging.StreamHandler()

    # Establece INFO como nivel mínimo para los mensajes
    # que aparecerán en la terminal.
    console_handler.setLevel(logging.INFO)

    # Define el formato de los mensajes que aparecerán
    # en la terminal.
    console_handler.setFormatter(
        logging.Formatter(
            LOG_FORMAT,
            datefmt=DATE_FORMAT
        )
    )


    # ========================================================
    # REGISTRAR LOS HANDLERS
    # ========================================================

    # Agrega el handler de archivo al logger.
    #
    # A partir de este momento, los logs también se guardarán
    # en logs/app.log.
    logger.addHandler(file_handler)

    # Agrega el handler de consola al logger.
    #
    # A partir de este momento, los logs también aparecerán
    # en la terminal.
    logger.addHandler(console_handler)