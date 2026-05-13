from cliente import Cliente  # importa la clase o excepción necesaria
from servicio import (  # importa la clase o excepción necesaria
    ReservaSala,  # ejecuta la instrucción correspondiente
    AlquilerEquipo,  # ejecuta la instrucción correspondiente
    AsesoriaEspecializada,  # ejecuta la instrucción correspondiente
    ServicioError  # ejecuta la instrucción correspondiente
)  # ejecuta la instrucción correspondiente
from reserva import Reserva  # importa la clase o excepción necesaria
from excepciones import ClienteError, ReservaError  # importa la clase o excepción necesaria
from logger_config import logger  # importa la clase o excepción necesaria


def ejecutar_demo():  # define el método principal de demostración
    clientes = []  # asigna un valor a una variable o atributo
    servicios = []  # asigna un valor a una variable o atributo
    reservas = []  # asigna un valor a una variable o atributo

    print("=== DEMOSTRACIÓN DEL SISTEMA SOFTWARE FJ ===")  # muestra texto en la consola

    try:  # inicia un bloque try para manejo de excepciones
        cliente1 = Cliente("Juan", "juan@gmail.com")  # asigna un valor a una variable o atributo
        clientes.append(cliente1)  # agrega un elemento a la lista
        logger.info(f"Cliente registrado: {cliente1.mostrar_info()}")  # registra un evento informativo en el log
        print("Cliente registrado:", cliente1.mostrar_info())  # muestra texto en la consola
    except ClienteError as e:  # captura la excepción lanzada en el bloque try
        logger.error(e)  # registra un error en el log
        print("Error de cliente:", e)  # muestra texto en la consola
    finally:  # se ejecuta siempre después del bloque try/except
        print("Fin de operación 1\n")  # muestra texto en la consola

    try:  # inicia un bloque try para manejo de excepciones
        Cliente("", "ana@gmail.com")  # ejecuta la instrucción correspondiente
    except ClienteError as e:  # captura la excepción lanzada en el bloque try
        logger.error(e)  # registra un error en el log
        print("Cliente inválido detectado:", e)  # muestra texto en la consola

    try:  # inicia un bloque try para manejo de excepciones
        Cliente("Ana", "correo_invalido")  # ejecuta la instrucción correspondiente
    except ClienteError as e:  # captura la excepción lanzada en el bloque try
        logger.error(e)  # registra un error en el log
        print("Cliente inválido detectado:", e)  # muestra texto en la consola

    try:  # inicia un bloque try para manejo de excepciones
        sala = ReservaSala("Sala Premium", 50, 4)  # asigna un valor a una variable o atributo
        servicios.append(sala)  # agrega un elemento a la lista
        logger.info(f"Servicio creado: {sala.mostrar_info()}")  # registra un evento informativo en el log
        print("Servicio creado:", sala.describir_servicio())  # muestra texto en la consola
    except ServicioError as e:  # captura la excepción lanzada en el bloque try
        logger.error(e)  # registra un error en el log
        print("Error de servicio:", e)  # muestra texto en la consola

    try:  # inicia un bloque try para manejo de excepciones
        ReservaSala("Sala Económica", -20, 3)  # ejecuta la instrucción correspondiente
    except ServicioError as e:  # captura la excepción lanzada en el bloque try
        logger.error(e)  # registra un error en el log
        print("Servicio inválido detectado:", e)  # muestra texto en la consola

    try:  # inicia un bloque try para manejo de excepciones
        equipo = AlquilerEquipo("PC Gamer", 100, 3)  # asigna un valor a una variable o atributo
        servicios.append(equipo)  # agrega un elemento a la lista
        logger.info(f"Servicio creado: {equipo.mostrar_info()}")  # registra un evento informativo en el log
        print("Servicio creado:", equipo.describir_servicio())  # muestra texto en la consola
    except ServicioError as e:  # captura la excepción lanzada en el bloque try
        logger.error(e)  # registra un error en el log
        print("Error de servicio:", e)  # muestra texto en la consola

    try:  # inicia un bloque try para manejo de excepciones
        asesoria = AsesoriaEspecializada("Consultoría Python", 150, 2, "Carlos")  # asigna un valor a una variable o atributo
        servicios.append(asesoria)  # agrega un elemento a la lista
        logger.info(f"Servicio creado: {asesoria.mostrar_info()}")  # registra un evento informativo en el log
        print("Servicio creado:", asesoria.describir_servicio())  # muestra texto en la consola
    except ServicioError as e:  # captura la excepción lanzada en el bloque try
        logger.error(e)  # registra un error en el log
        print("Error de servicio:", e)  # muestra texto en la consola

    try:  # inicia un bloque try para manejo de excepciones
        reserva1 = Reserva(cliente1, sala)  # asigna un valor a una variable o atributo
        reserva1.procesar()  # ejecuta la instrucción correspondiente
        reservas.append(reserva1)  # agrega un elemento a la lista
        print("Reserva realizada:", reserva1.mostrar_reserva())  # muestra texto en la consola
    except (ReservaError, ClienteError, ServicioError) as e:  # captura la excepción lanzada en el bloque try
        logger.error(e)  # registra un error en el log
        print("Error en la reserva:", e)  # muestra texto en la consola

    try:  # inicia un bloque try para manejo de excepciones
        reserva1.confirmar()  # ejecuta la instrucción correspondiente
    except ReservaError as e:  # captura la excepción lanzada en el bloque try
        logger.error(e)  # registra un error en el log
        print("Error detectado en doble confirmación:", e)  # muestra texto en la consola

    try:  # inicia un bloque try para manejo de excepciones
        Reserva(cliente1, None)  # ejecuta la instrucción correspondiente
    except ReservaError as e:  # captura la excepción lanzada en el bloque try
        logger.error(e)  # registra un error en el log
        print("Reserva inválida detectada:", e)  # muestra texto en la consola

    try:  # inicia un bloque try para manejo de excepciones
        reserva1.cancelar()  # ejecuta la instrucción correspondiente
        print("Reserva cancelada exitosamente")  # muestra texto en la consola
        reserva1.cancelar()  # ejecuta la instrucción correspondiente
    except ReservaError as e:  # captura la excepción lanzada en el bloque try
        logger.error(e)  # registra un error en el log
        print("Error detectado en doble cancelación:", e)  # muestra texto en la consola

    print("\n=== RESUMEN DE OPERACIONES ===")  # muestra texto en la consola
    print(f"Clientes válidos registrados: {len(clientes)}")  # muestra texto en la consola
    print(f"Servicios válidos creados: {len(servicios)}")  # muestra texto en la consola
    print(f"Reservas procesadas: {len(reservas)}")  # muestra texto en la consola
    logger.info(f"Resumen: {len(clientes)} clientes, {len(servicios)} servicios, {len(reservas)} reservas")  # registra un evento informativo en el log


if __name__ == "__main__":  # evalúa una condición para decidir el flujo
    ejecutar_demo()  # ejecuta la instrucción correspondiente
