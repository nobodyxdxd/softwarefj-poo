import re
from excepciones import ClienteError


class Cliente:

    def __init__(self, nombre, correo):

        self.__nombre = nombre
        self.__correo = correo

        self.validar()

    def validar(self):

        if not self.__nombre.strip():
            raise ClienteError("El nombre está vacío")

        # Validación mejorada de correo con regex
        patron_correo = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(patron_correo, self.__correo):
            raise ClienteError("Correo inválido. Debe tener formato: usuario@dominio.com")

    def get_nombre(self):
        return self.__nombre

    def get_correo(self):
        return self.__correo

    def mostrar_info(self):
        return f"{self.__nombre} - {self.__correo}"