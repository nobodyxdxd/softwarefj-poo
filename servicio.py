from abc import ABC, abstractmethod


class Servicio(ABC):

    def __init__(self, nombre, precio_base):

        self.nombre = nombre
        self.precio_base = precio_base

    @abstractmethod
    def calcular_costo(self):
        pass

    @abstractmethod
    def describir_servicio(self):
        pass


class ReservaSala(Servicio):

    def __init__(self, nombre, precio_base, horas):

        super().__init__(nombre, precio_base)

        self.horas = horas

    def calcular_costo(self, impuesto=0, descuento=0):

        total = self.precio_base * self.horas

        total += total * impuesto

        total -= descuento

        return total

    def describir_servicio(self):

        return f"Reserva de sala por {self.horas} horas"


class AlquilerEquipo(Servicio):

    def __init__(self, nombre, precio_base, dias):

        super().__init__(nombre, precio_base)

        self.dias = dias

    def calcular_costo(self):

        return self.precio_base * self.dias

    def describir_servicio(self):

        return f"Alquiler de equipo por {self.dias} días"


class AsesoriaEspecializada(Servicio):

    def __init__(self, nombre, precio_base, horas, especialista):

        super().__init__(nombre, precio_base)

        self.horas = horas
        self.especialista = especialista

    def calcular_costo(self):

        return self.precio_base * self.horas

    def describir_servicio(self):

        return f"Asesoría especializada con {self.especialista} por {self.horas} horas"