import time
from threading import Lock


class Metrics:
    """
    Clase encargada de almacenar y calcular
    las métricas de comportamiento de la aplicación.
    """

    def __init__(self):
        # Cantidad total de solicitudes HTTP recibidas
        self.total_requests = 0

        # Cantidad de solicitudes procesadas correctamente
        self.successful_requests = 0

        # Cantidad de solicitudes que terminaron con algún error
        self.error_requests = 0

        # Cantidad de errores causados por datos inválidos
        self.validation_errors = 0

        # Cantidad de errores HTTP 404
        # Por ejemplo, cuando se consulta un producto inexistente
        self.not_found_errors = 0

        # Cantidad de errores internos HTTP 500
        self.internal_errors = 0

        # Suma acumulada del tiempo de respuesta
        # Se almacena en milisegundos
        self.total_response_time = 0.0

        # Lock utilizado para evitar problemas de concurrencia.
        # Esto permite que varias solicitudes no modifiquen
        # las métricas simultáneamente de forma incorrecta.
        self.lock = Lock()

    def register_request(self, status_code, response_time):
        """
        Registra el resultado de una solicitud HTTP.

        Parámetros:
        status_code:
            Código HTTP devuelto por la aplicación.

        response_time:
            Tiempo que tardó la solicitud en responder,
            expresado en milisegundos.
        """

        # Se utiliza el Lock para proteger los datos
        # mientras son modificados.
        with self.lock:

            # Incrementa el contador de solicitudes totales
            self.total_requests += 1

            # Acumula el tiempo de respuesta de la solicitud
            self.total_response_time += response_time

            # Los códigos entre 200 y 399 se consideran
            # solicitudes procesadas correctamente.
            if 200 <= status_code < 400:

                self.successful_requests += 1

            else:

                # Si el código es 400 o superior,
                # se registra como una solicitud con error.
                self.error_requests += 1

                # Verifica si el error corresponde a un 404.
                if status_code == 404:

                    self.not_found_errors += 1

                # Verifica si el error corresponde a un 500.
                elif status_code == 500:

                    self.internal_errors += 1

    def register_validation_error(self):
        """
        Registra un error producido por información
        inválida enviada por el cliente.

        Por ejemplo:
        - Campos obligatorios faltantes.
        - Precio menor o igual a cero.
        - Stock negativo.
        - Tipos de datos incorrectos.
        """

        # Protege el contador frente a accesos simultáneos
        with self.lock:

            # Incrementa la cantidad de errores de validación
            self.validation_errors += 1

    def get_metrics(self):
        """
        Calcula y devuelve las métricas actuales
        de la aplicación.
        """

        # Protege la lectura de las métricas
        # mientras otros procesos pueden estar modificándolas.
        with self.lock:

            # Verifica que exista al menos una solicitud
            # antes de realizar divisiones.
            if self.total_requests > 0:

                # Calcula el porcentaje de solicitudes exitosas.
                #
                # Fórmula:
                # solicitudes exitosas / solicitudes totales * 100
                success_rate = (
                    self.successful_requests
                    / self.total_requests
                ) * 100

                # Calcula el porcentaje de solicitudes con error.
                #
                # Fórmula:
                # solicitudes con error / solicitudes totales * 100
                error_rate = (
                    self.error_requests
                    / self.total_requests
                ) * 100

                # Calcula el tiempo promedio de respuesta.
                #
                # Fórmula:
                # tiempo total / solicitudes totales
                average_response_time = (
                    self.total_response_time
                    / self.total_requests
                )

            else:

                # Si todavía no se han recibido solicitudes,
                # todas las métricas calculadas comienzan en cero.
                success_rate = 0
                error_rate = 0
                average_response_time = 0

            # Devuelve todas las métricas en forma de diccionario.
            return {

                # Número total de solicitudes procesadas
                "total_requests": self.total_requests,

                # Número de solicitudes exitosas
                "successful_requests": self.successful_requests,

                # Número de solicitudes con error
                "error_requests": self.error_requests,

                # Número de errores de validación
                "validation_errors": self.validation_errors,

                # Número de errores 404
                "not_found_errors": self.not_found_errors,

                # Número de errores 500
                "internal_errors": self.internal_errors,

                # Porcentaje de solicitudes exitosas
                # Redondeado a dos decimales
                "success_rate_percent": round(
                    success_rate,
                    2
                ),

                # Porcentaje de solicitudes con error
                # Redondeado a dos decimales
                "error_rate_percent": round(
                    error_rate,
                    2
                ),

                # Tiempo promedio de respuesta en milisegundos
                # Redondeado a dos decimales
                "average_response_time_ms": round(
                    average_response_time,
                    2
                )
            }


# Se crea una única instancia de la clase Metrics.
#
# Esta instancia será utilizada por toda la aplicación
# para mantener las métricas acumuladas.
metrics = Metrics()