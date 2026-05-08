from excepciones import ClienteError


class Cliente:

    def __init__(self, nombre, correo):

        self.__nombre = nombre
        self.__correo = correo

        self.validar()

    def validar(self):

        if not self.__nombre.strip():
            raise ClienteError("El nombre está vacío")

        if "@" not in self.__correo:
            raise ClienteError("Correo inválido")

    def get_nombre(self):
        return self.__nombre

    def get_correo(self):
        return self.__correo

    def mostrar_info(self):
        return f"{self.__nombre} - {self.__correo}"