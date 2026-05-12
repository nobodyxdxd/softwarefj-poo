from cliente import Cliente
from servicio import (
    ReservaSala,
    AlquilerEquipo,
    AsesoriaEspecializada,
    ServicioError
)
from reserva import Reserva
from excepciones import ClienteError, ReservaError
from logger_config import logger


def ejecutar_demo():
    clientes = []
    servicios = []
    reservas = []

    print("=== DEMOSTRACIÓN DEL SISTEMA SOFTWARE FJ ===")

    try:
        cliente1 = Cliente("Juan", "juan@gmail.com")
        clientes.append(cliente1)
        logger.info(f"Cliente registrado: {cliente1.mostrar_info()}")
        print("Cliente registrado:", cliente1.mostrar_info())
    except ClienteError as e:
        logger.error(e)
        print("Error de cliente:", e)
    finally:
        print("Fin de operación 1\n")

    try:
        Cliente("", "ana@gmail.com")
    except ClienteError as e:
        logger.error(e)
        print("Cliente inválido detectado:", e)

    try:
        Cliente("Ana", "correo_invalido")
    except ClienteError as e:
        logger.error(e)
        print("Cliente inválido detectado:", e)

    try:
        sala = ReservaSala("Sala Premium", 50, 4)
        servicios.append(sala)
        logger.info(f"Servicio creado: {sala.mostrar_info()}")
        print("Servicio creado:", sala.describir_servicio())
    except ServicioError as e:
        logger.error(e)
        print("Error de servicio:", e)

    try:
        ReservaSala("Sala Económica", -20, 3)
    except ServicioError as e:
        logger.error(e)
        print("Servicio inválido detectado:", e)

    try:
        equipo = AlquilerEquipo("PC Gamer", 100, 3)
        servicios.append(equipo)
        logger.info(f"Servicio creado: {equipo.mostrar_info()}")
        print("Servicio creado:", equipo.describir_servicio())
    except ServicioError as e:
        logger.error(e)
        print("Error de servicio:", e)

    try:
        asesoria = AsesoriaEspecializada("Consultoría Python", 150, 2, "Carlos")
        servicios.append(asesoria)
        logger.info(f"Servicio creado: {asesoria.mostrar_info()}")
        print("Servicio creado:", asesoria.describir_servicio())
    except ServicioError as e:
        logger.error(e)
        print("Error de servicio:", e)

    try:
        reserva1 = Reserva(cliente1, sala)
        reserva1.procesar()
        reservas.append(reserva1)
        print("Reserva realizada:", reserva1.mostrar_reserva())
    except (ReservaError, ClienteError, ServicioError) as e:
        logger.error(e)
        print("Error en la reserva:", e)

    try:
        reserva1.confirmar()
    except ReservaError as e:
        logger.error(e)
        print("Error detectado en doble confirmación:", e)

    try:
        Reserva(cliente1, None)
    except ReservaError as e:
        logger.error(e)
        print("Reserva inválida detectada:", e)

    try:
        reserva1.cancelar()
        print("Reserva cancelada exitosamente")
        reserva1.cancelar()
    except ReservaError as e:
        logger.error(e)
        print("Error detectado en doble cancelación:", e)

    print("\n=== RESUMEN DE OPERACIONES ===")
    print(f"Clientes válidos registrados: {len(clientes)}")
    print(f"Servicios válidos creados: {len(servicios)}")
    print(f"Reservas procesadas: {len(reservas)}")
    logger.info(f"Resumen: {len(clientes)} clientes, {len(servicios)} servicios, {len(reservas)} reservas")


if __name__ == "__main__":
    ejecutar_demo()
