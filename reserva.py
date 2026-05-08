from excepciones import ReservaError
from logger_config import logger


class Reserva:

    def __init__(self, cliente, servicio):

        self.cliente = cliente
        self.servicio = servicio
        self.estado = "Pendiente"

    def confirmar(self):

        try:

            if self.estado == "Confirmada":

                raise ValueError("Intento doble de confirmación")

            self.estado = "Confirmada"

            print("Reserva confirmada")

        except ValueError as e:

            logger.error(e)

            raise ReservaError(
                "Error al confirmar la reserva"
            ) from e

    def cancelar(self):

        if self.estado == "Cancelada":

            raise ReservaError("La reserva ya está cancelada")

        self.estado = "Cancelada"

        print("Reserva cancelada")

    def mostrar_reserva(self):

        return (
            f"Cliente: {self.cliente.get_nombre()} | "
            f"Servicio: {self.servicio.nombre} | "
            f"Estado: {self.estado}"
        )