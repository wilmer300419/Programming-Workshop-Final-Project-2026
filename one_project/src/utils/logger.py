import logging
import os
from logging.handlers import RotatingFileHandler


# Crear la carpeta logs si no existe
LOG_DIR = "logs"

os.makedirs(LOG_DIR, exist_ok=True)


# Formato de los logs
LOG_FORMAT = (
    "%(asctime)s %(levelname)s "
    "%(message)s"
)


# Formato de fecha
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


# Logger principal de la aplicación
logger = logging.getLogger("product_api")

logger.setLevel(logging.INFO)


# Evitar agregar handlers varias veces
if not logger.handlers:

    # Handler para guardar los logs en archivo
    file_handler = RotatingFileHandler(
        "logs/app.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8"
    )

    file_handler.setLevel(logging.INFO)

    file_handler.setFormatter(
        logging.Formatter(
            LOG_FORMAT,
            datefmt=DATE_FORMAT
        )
    )


    # Handler para mostrar los logs en la terminal
    console_handler = logging.StreamHandler()

    console_handler.setLevel(logging.INFO)

    console_handler.setFormatter(
        logging.Formatter(
            LOG_FORMAT,
            datefmt=DATE_FORMAT
        )
    )


    # Registrar los handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
