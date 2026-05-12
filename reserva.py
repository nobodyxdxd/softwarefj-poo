from excepciones import ReservaError
from logger_config import logger


class Reserva:

    def __init__(self, cliente, servicio):
        self.cliente = cliente
        self.servicio = servicio
        self.estado = "Pendiente"
        self.historial = []
        self.validar()

    def validar(self):
        if self.cliente is None:
            raise ReservaError("El cliente para la reserva no puede ser nulo")

        if self.servicio is None:
            raise ReservaError("El servicio para la reserva no puede ser nulo")

        if not hasattr(self.servicio, "calcular_costo"):
            raise ReservaError("El servicio no es válido para una reserva")

    def confirmar(self):
        try:
            if self.estado == "Confirmada":
                raise ValueError("Intento doble de confirmación")

            self.estado = "Confirmada"
            self.historial.append("Confirmada")
            logger.info(
                f"Reserva confirmada: {self.cliente.get_nombre()} -> {self.servicio.nombre}"
            )
        except ValueError as e:
            logger.error(e)
            raise ReservaError("Error al confirmar la reserva") from e

    def cancelar(self):
        if self.estado == "Cancelada":
            raise ReservaError("La reserva ya está cancelada")

        self.estado = "Cancelada"
        self.historial.append("Cancelada")
        logger.info(
            f"Reserva cancelada: {self.cliente.get_nombre()} -> {self.servicio.nombre}"
        )

    def procesar(self):
        try:
            if self.estado != "Pendiente":
                raise ReservaError("Solo las reservas pendientes se pueden procesar")

            self.confirmar()
        except ReservaError as e:
            logger.error(e)
            raise
        else:
            logger.info("Reserva procesada correctamente")
        finally:
            logger.info(f"Estado final de la reserva: {self.estado}")

    def editar_estado(self, nuevo_estado):
        """Permite editar el estado de una reserva."""
        if nuevo_estado not in ["Pendiente", "Confirmada", "Cancelada"]:
            raise ReservaError(f"Estado inválido: {nuevo_estado}")
        self.estado = nuevo_estado
        self.historial.append(nuevo_estado)
        logger.info(f"Reserva modificada. Nuevo estado: {nuevo_estado}")

    def obtener_costo_total(self, impuesto=0, descuento=0):
        """Calcula el costo total de la reserva."""
        return self.servicio.calcular_costo(impuesto, descuento)

    def mostrar_reserva(self):
        duracion = getattr(self.servicio, "horas", None) or getattr(self.servicio, "dias", None)
        detalle_servicio = self.servicio.describir_servicio()

        return (
            f"Cliente: {self.cliente.get_nombre()} | "
            f"Cédula: {self.cliente.get_cedula()} | "
            f"Servicio: {self.servicio.nombre} | "
            f"Detalle: {detalle_servicio} | "
            f"Duración: {duracion} | "
            f"Costo: ${self.obtener_costo_total():,.0f} | "
            f"Estado: {self.estado}"
        )

