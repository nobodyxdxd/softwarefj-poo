from excepciones import ReservaError  # importa la clase o excepción necesaria
from logger_config import logger  # importa la clase o excepción necesaria


class Reserva:  # declara la clase

    def __init__(self, cliente, servicio):  # define el constructor de la clase
        self.cliente = cliente  # asigna un valor a una variable o atributo
        self.servicio = servicio  # asigna un valor a una variable o atributo
        self.estado = "Pendiente"  # asigna un valor a una variable o atributo
        self.historial = []  # asigna un valor a una variable o atributo
        self.validar()  # ejecuta la instrucción correspondiente

    def validar(self):  # define el método validar de la clase
        if self.cliente is None:  # evalúa una condición para decidir el flujo
            raise ReservaError("El cliente para la reserva no puede ser nulo")  # lanza una excepción cuando ocurre un error

        if self.servicio is None:  # evalúa una condición para decidir el flujo
            raise ReservaError("El servicio para la reserva no puede ser nulo")  # lanza una excepción cuando ocurre un error

        if not hasattr(self.servicio, "calcular_costo"):  # evalúa una condición para decidir el flujo
            raise ReservaError("El servicio no es válido para una reserva")  # lanza una excepción cuando ocurre un error

    def confirmar(self):  # define el método para confirmar la reserva
        try:  # inicia un bloque try para manejo de excepciones
            if self.estado == "Confirmada":  # verifica si la reserva ya estaba confirmada
                raise ValueError("Intento doble de confirmación")  # lanza una excepción cuando ocurre un error

            self.estado = "Confirmada"  # asigna un valor a una variable o atributo
            self.historial.append("Confirmada")  # agrega un elemento a la lista
            logger.info(  # registra un evento informativo en el log
                f"Reserva confirmada: {self.cliente.get_nombre()} -> {self.servicio.nombre}"  # ejecuta la instrucción correspondiente
            )  # ejecuta la instrucción correspondiente
        except ValueError as e:  # captura la excepción lanzada en el bloque try
            logger.error(e)  # registra un error en el log
            raise ReservaError("Error al confirmar la reserva") from e  # lanza una excepción cuando ocurre un error

    def cancelar(self):  # define el método para cancelar la reserva
        if self.estado == "Cancelada":  # verifica si la reserva ya estaba cancelada
            raise ReservaError("La reserva ya está cancelada")  # lanza una excepción cuando ocurre un error

        self.estado = "Cancelada"  # asigna un valor a una variable o atributo
        self.historial.append("Cancelada")  # agrega un elemento a la lista
        logger.info(  # registra un evento informativo en el log
            f"Reserva cancelada: {self.cliente.get_nombre()} -> {self.servicio.nombre}"  # ejecuta la instrucción correspondiente
        )  # ejecuta la instrucción correspondiente

    def procesar(self):  # define el método para procesar la reserva
        try:  # inicia un bloque try para manejo de excepciones
            if self.estado != "Pendiente":  # verifica que la reserva esté en estado pendiente
                raise ReservaError("Solo las reservas pendientes se pueden procesar")  # lanza una excepción cuando ocurre un error

            self.confirmar()  # ejecuta la instrucción correspondiente
        except ReservaError as e:  # captura la excepción lanzada en el bloque try
            logger.error(e)  # registra un error en el log
            raise  # ejecuta la instrucción correspondiente
        else:  # se ejecuta cuando no ocurre una excepción
            logger.info("Reserva procesada correctamente")  # registra un evento informativo en el log
        finally:  # se ejecuta siempre después del bloque try/except
            logger.info(f"Estado final de la reserva: {self.estado}")  # registra un evento informativo en el log

    def editar_estado(self, nuevo_estado):  # define el método para editar el estado de la reserva
        """Permite editar el estado de una reserva."""
        if nuevo_estado not in ["Pendiente", "Confirmada", "Cancelada"]:  # evalúa una condición para decidir el flujo
            raise ReservaError(f"Estado inválido: {nuevo_estado}")  # lanza una excepción cuando ocurre un error
        self.estado = nuevo_estado  # asigna un valor a una variable o atributo
        self.historial.append(nuevo_estado)  # agrega un elemento a la lista
        logger.info(f"Reserva modificada. Nuevo estado: {nuevo_estado}")  # registra un evento informativo en el log

    def obtener_costo_total(self, impuesto=0, descuento=0):  # define el método para obtener el costo total
        """Calcula el costo total de la reserva."""
        return self.servicio.calcular_costo(impuesto, descuento)  # devuelve el resultado desde la función o método

    def mostrar_reserva(self):  # define el método para mostrar los datos de la reserva
        duracion = getattr(self.servicio, "horas", None) or getattr(self.servicio, "dias", None)  # asigna un valor a una variable o atributo
        detalle_servicio = self.servicio.describir_servicio()  # asigna un valor a una variable o atributo

        return (  # devuelve el resultado desde la función o método
            f"Cliente: {self.cliente.get_nombre()} | "  # ejecuta la instrucción correspondiente
            f"Cédula: {self.cliente.get_cedula()} | "  # ejecuta la instrucción correspondiente
            f"Servicio: {self.servicio.nombre} | "  # ejecuta la instrucción correspondiente
            f"Detalle: {detalle_servicio} | "  # ejecuta la instrucción correspondiente
            f"Duración: {duracion} | "  # ejecuta la instrucción correspondiente
            f"Costo: ${self.obtener_costo_total():,.0f} | "  # ejecuta la instrucción correspondiente
            f"Estado: {self.estado}"  # ejecuta la instrucción correspondiente
        )  # ejecuta la instrucción correspondiente

