from cliente import Cliente
from servicio import (
    ReservaSala,
    AlquilerEquipo,
    AsesoriaEspecializada
)
from reserva import Reserva
from logger_config import logger


try:

    cliente1 = Cliente("Juan", "juan@gmail.com")

except Exception as e:

    logger.error(e)

    print("Error:", e)

else:

    print(cliente1.mostrar_info())

    print("Cliente registrado correctamente")

finally:

    print("Proceso de cliente finalizado")


print("\n--- SERVICIOS ---")


sala = ReservaSala("Sala Premium", 50, 4)

print(sala.describir_servicio())

print("Costo:", sala.calcular_costo())

print("Costo con impuesto:", sala.calcular_costo(impuesto=0.19))

print("Costo con descuento:", sala.calcular_costo(descuento=20))


equipo = AlquilerEquipo("PC Gamer", 100, 3)

print(equipo.describir_servicio())

print("Costo:", equipo.calcular_costo())


asesoria = AsesoriaEspecializada(
    "Consultoría Python",
    150,
    2,
    "Carlos"
)

print(asesoria.describir_servicio())

print("Costo:", asesoria.calcular_costo())


print("\n--- RESERVA ---")


reserva1 = Reserva(cliente1, sala)

print(reserva1.mostrar_reserva())

reserva1.confirmar()

print(reserva1.mostrar_reserva())


print("\n--- PRUEBAS DE ERRORES ---")


try:

    cliente_malo = Cliente("", "correo_malo")

except Exception as e:

    logger.error(e)

    print("Error detectado:", e)


try:

    reserva1.confirmar()

except Exception as e:

    logger.error(e)

    print("Error detectado:", e)


try:

    reserva1.cancelar()

    reserva1.cancelar()

except Exception as e:

    logger.error(e)

    print("Error detectado:", e)