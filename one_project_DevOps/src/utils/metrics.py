import os
import re


# ============================================================
# CONFIGURACIÓN
# ============================================================

# Obtiene la carpeta donde se encuentra este archivo.
BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

# Sube desde:
#
# src/utils/metrics.py
#
# hasta:
#
# proyecto/
#
PROJECT_DIR = os.path.dirname(
    os.path.dirname(BASE_DIR)
)

# Carpeta donde se almacenan los logs.
LOG_DIR = os.path.join(
    PROJECT_DIR,
    "logs"
)


class Metrics:
    """
    Clase encargada de calcular las métricas
    leyendo directamente los archivos de logs.
    """

    def __init__(self):

        # Expresión regular utilizada para encontrar
        # las solicitudes terminadas.
        #
        # Ejemplo:
        #
        # SUCCESS GET /products - HTTP 200 - Tiempo: 5.32 ms
        #
        # ERROR GET /products/999 - HTTP 404 - Tiempo: 2.15 ms
        #
        self.log_pattern = re.compile(
            r"(SUCCESS|ERROR)\s+"
            r"([A-Z]+)\s+"
            r"(\S+)\s+-\s+"
            r"HTTP\s+(\d+)\s+-\s+"
            r"Tiempo:\s+([\d.]+)\s+ms"
        )


    def _get_log_files(self):
        """
        Obtiene todos los archivos de logs disponibles.

        Incluye:
            app.log
            app.log.1
            app.log.2
            app.log.3
        """

        if not os.path.exists(LOG_DIR):
            return []

        log_files = []

        for filename in os.listdir(LOG_DIR):

            # Solo toma archivos que comiencen
            # con app.log
            if filename.startswith("app.log"):

                file_path = os.path.join(
                    LOG_DIR,
                    filename
                )

                if os.path.isfile(file_path):
                    log_files.append(file_path)

        return log_files


    def get_metrics(self):
        """
        Lee los archivos de log y calcula
        las métricas actuales.

        Las métricas se calculan nuevamente
        cada vez que se consulta /metrics.
        """

        # ====================================================
        # CONTADORES
        # ====================================================

        total_requests = 0

        successful_requests = 0

        error_requests = 0

        bad_request_errors = 0

        validation_errors = 0

        not_found_errors = 0

        internal_errors = 0

        total_response_time = 0.0


        # ====================================================
        # OBTENER ARCHIVOS DE LOG
        # ====================================================

        log_files = self._get_log_files()


        # ====================================================
        # LEER LOS LOGS
        # ====================================================

        for log_file in log_files:

            try:

                with open(
                    log_file,
                    "r",
                    encoding="utf-8"
                ) as file:

                    for line in file:

                        # Busca una línea que represente
                        # una solicitud finalizada.
                        match = self.log_pattern.search(
                            line
                        )

                        # Si la línea no coincide,
                        # simplemente se ignora.
                        if not match:
                            continue


                        # Obtiene los datos encontrados.
                        log_type = match.group(1)

                        method = match.group(2)

                        path = match.group(3)

                        status_code = int(
                            match.group(4)
                        )

                        response_time = float(
                            match.group(5)
                        )


                        # =================================================
                        # EXCLUIR /metrics
                        # =================================================

                        # No contamos la consulta de métricas
                        # para evitar que /metrics se cuente
                        # a sí mismo.
                        if path == "/metrics":
                            continue


                        # =================================================
                        # MÉTRICAS GENERALES
                        # =================================================

                        total_requests += 1

                        total_response_time += (
                            response_time
                        )


                        # =================================================
                        # SOLICITUD EXITOSA
                        # =================================================

                        if 200 <= status_code < 400:

                            successful_requests += 1


                        # =================================================
                        # SOLICITUD CON ERROR
                        # =================================================

                        else:

                            error_requests += 1


                            # HTTP 400
                            if status_code == 400:

                                bad_request_errors += 1


                            # HTTP 422
                            elif status_code == 422:

                                validation_errors += 1


                            # HTTP 404
                            elif status_code == 404:

                                not_found_errors += 1


                            # HTTP 500
                            elif status_code == 500:

                                internal_errors += 1


            except OSError:
                # Si un archivo no puede ser leído,
                # continúa con los demás archivos.
                continue


        # ====================================================
        # CÁLCULO DE PORCENTAJES
        # ====================================================

        if total_requests > 0:

            success_rate = (
                successful_requests
                / total_requests
            ) * 100

            error_rate = (
                error_requests
                / total_requests
            ) * 100

            average_response_time = (
                total_response_time
                / total_requests
            )

        else:

            success_rate = 0

            error_rate = 0

            average_response_time = 0


        # ====================================================
        # RESULTADO
        # ====================================================

        return {

            "total_requests":
                total_requests,

            "successful_requests":
                successful_requests,

            "error_requests":
                error_requests,

            "bad_request_errors":
                bad_request_errors,

            "validation_errors":
                validation_errors,

            "not_found_errors":
                not_found_errors,

            "internal_errors":
                internal_errors,

            "success_rate_percent":
                round(
                    success_rate,
                    2
                ),

            "error_rate_percent":
                round(
                    error_rate,
                    2
                ),

            "average_response_time_ms":
                round(
                    average_response_time,
                    2
                )
        }


# ============================================================
# INSTANCIA GLOBAL
# ============================================================

metrics = Metrics()