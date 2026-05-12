from entidad import Entidad
from excepciones import ServicioError


class Servicio(Entidad):

    def __init__(self, nombre, precio_base):
        self.__nombre = nombre
        self.__precio_base = precio_base
        self.validar()

    @property
    def nombre(self):
        return self.__nombre

    @property
    def precio_base(self):
        return self.__precio_base

    def validar(self):
        if not isinstance(self.__nombre, str) or not self.__nombre.strip():
            raise ServicioError("El nombre del servicio es obligatorio")

        if not isinstance(self.__precio_base, (int, float)) or self.__precio_base <= 0:
            raise ServicioError("El precio base del servicio debe ser mayor a cero")

    def mostrar_info(self):
        return f"{self.nombre} - ${self.precio_base:,.0f}"

    def calcular_costo(self, impuesto=0, descuento=0):
        raise ServicioError("El servicio no implementa el cálculo de costo")

    def describir_servicio(self):
        raise ServicioError("El servicio no implementa descripción")


class ReservaSala(Servicio):

    def __init__(self, nombre, precio_base, horas):
        self.horas = horas
        super().__init__(nombre, precio_base)
        self.validar()

    def validar(self):
        super().validar()
        if not isinstance(self.horas, int) or self.horas <= 0:
            raise ServicioError("La duración de la reserva debe ser un número de horas mayor a cero")

    def calcular_costo(self, impuesto=0, descuento=0):
        total = self.precio_base * self.horas
        if impuesto < 0 or descuento < 0:
            raise ServicioError("Impuesto y descuento deben ser valores no negativos")
        total += total * impuesto
        total -= descuento
        return total

    def describir_servicio(self):
        return f"Reserva de sala por {self.horas} horas"


class AlquilerEquipo(Servicio):

    def __init__(self, nombre, precio_base, dias):
        self.dias = dias
        super().__init__(nombre, precio_base)
        self.validar()

    def validar(self):
        super().validar()
        if not isinstance(self.dias, int) or self.dias <= 0:
            raise ServicioError("Los días de alquiler deben ser un número entero mayor a cero")

    def calcular_costo(self, impuesto=0, descuento=0):
        total = self.precio_base * self.dias
        if impuesto < 0 or descuento < 0:
            raise ServicioError("Impuesto y descuento deben ser valores no negativos")
        return total + total * impuesto - descuento

    def describir_servicio(self):
        return f"Alquiler de equipo por {self.dias} días"


class AsesoriaEspecializada(Servicio):

    def __init__(self, nombre, precio_base, horas, especialista):
        self.horas = horas
        self.especialista = especialista
        super().__init__(nombre, precio_base)
        self.validar()

    def validar(self):
        super().validar()
        if not isinstance(self.horas, int) or self.horas <= 0:
            raise ServicioError("La duración de la asesoría debe ser un número de horas mayor a cero")
        if not isinstance(self.especialista, str) or not self.especialista.strip():
            raise ServicioError("El especialista debe ser un nombre válido")

    def calcular_costo(self, impuesto=0, descuento=0):
        total = self.precio_base * self.horas
        if impuesto < 0 or descuento < 0:
            raise ServicioError("Impuesto y descuento deben ser valores no negativos")
        return total + total * impuesto - descuento

    def describir_servicio(self):
        return f"Asesoría especializada con {self.especialista} por {self.horas} horas"
