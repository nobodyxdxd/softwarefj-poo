import re
from entidad import Entidad
from excepciones import ClienteError


class Cliente(Entidad):

    _contador = 0
    _cedulas_registradas = set()

    def __init__(self, nombre, correo, cedula):
        self.__nombre = nombre
        self.__correo = correo
        self.__cedula = cedula
        Cliente._contador += 1
        self.__id = Cliente._contador
        self.validar()
        Cliente._cedulas_registradas.add(cedula)

    def validar(self):
        if not isinstance(self.__nombre, str) or not self.__nombre.strip():
            raise ClienteError("El nombre está vacío o no es válido")

        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚ ]+$", self.__nombre):
            raise ClienteError("El nombre solo puede contener letras y espacios")

        if not isinstance(self.__correo, str):
            raise ClienteError("El correo debe ser un texto válido")

        patron_correo = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(patron_correo, self.__correo):
            raise ClienteError("Correo inválido. Debe tener formato: usuario@dominio.com")

        if not isinstance(self.__cedula, str) or not self.__cedula.strip():
            raise ClienteError("La cédula es obligatoria")

        if not re.match(r"^\d+$", self.__cedula):
            raise ClienteError("La cédula solo debe contener números")

        if self.__cedula in Cliente._cedulas_registradas:
            raise ClienteError(f"La cédula {self.__cedula} ya está registrada")

    def get_nombre(self):
        return self.__nombre

    def get_correo(self):
        return self.__correo

    def get_cedula(self):
        return self.__cedula

    def get_id(self):
        return self.__id

    def mostrar_info(self):
        return f"ID: {self.__id} | Cédula: {self.__cedula} | {self.__nombre} | {self.__correo}"

    def __str__(self):
        return self.mostrar_info()

    @classmethod
    def buscar_por_cedula(cls, cedula):
        """Busca si una cédula ya está registrada."""
        return cedula in cls._cedulas_registradas
