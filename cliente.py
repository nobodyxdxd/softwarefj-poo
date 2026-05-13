import re  # importa el módulo o símbolo necesario
from entidad import Entidad  # importa la clase o excepción necesaria
from excepciones import ClienteError  # importa la clase o excepción necesaria


class Cliente(Entidad):  # declara la clase

    _contador = 0  # asigna un valor a una variable o atributo
    _cedulas_registradas = set()  # crea o actualiza un conjunto de valores

    def __init__(self, nombre, correo, cedula):  # define el constructor de la clase
        self.__nombre = nombre  # asigna un valor a una variable o atributo
        self.__correo = correo  # asigna un valor a una variable o atributo
        self.__cedula = cedula  # asigna un valor a una variable o atributo
        Cliente._contador += 1  # asigna un valor a una variable o atributo
        self.__id = Cliente._contador  # asigna un valor a una variable o atributo
        self.validar()  # ejecuta la instrucción correspondiente
        Cliente._cedulas_registradas.add(cedula)  # ejecuta la instrucción correspondiente

    def validar(self):  # define el método validar de la clase
        if not isinstance(self.__nombre, str) or not self.__nombre.strip():  # verifica que el valor sea del tipo esperado
            raise ClienteError("El nombre está vacío o no es válido")  # lanza una excepción cuando ocurre un error

        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚ ]+$", self.__nombre):  # verifica que el dato cumpla con el patrón definido
            raise ClienteError("El nombre solo puede contener letras y espacios")  # lanza una excepción cuando ocurre un error

        if not isinstance(self.__correo, str):  # verifica que el valor sea del tipo esperado
            raise ClienteError("El correo debe ser un texto válido")  # lanza una excepción cuando ocurre un error

        patron_correo = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'  # asigna un valor a una variable o atributo
        if not re.match(patron_correo, self.__correo):  # verifica que el dato cumpla con el patrón definido
            raise ClienteError("Correo inválido. Debe tener formato: usuario@dominio.com")  # lanza una excepción cuando ocurre un error

        if not isinstance(self.__cedula, str) or not self.__cedula.strip():  # verifica que el valor sea del tipo esperado
            raise ClienteError("La cédula es obligatoria")  # lanza una excepción cuando ocurre un error

        if not re.match(r"^\d+$", self.__cedula):  # verifica que el dato cumpla con el patrón definido
            raise ClienteError("La cédula solo debe contener números")  # lanza una excepción cuando ocurre un error

        if self.__cedula in Cliente._cedulas_registradas:  # evalúa una condición para decidir el flujo
            raise ClienteError(f"La cédula {self.__cedula} ya está registrada")  # lanza una excepción cuando ocurre un error

    def get_nombre(self):  # ejecuta la instrucción correspondiente
        return self.__nombre  # devuelve el resultado desde la función o método

    def get_correo(self):  # ejecuta la instrucción correspondiente
        return self.__correo  # devuelve el resultado desde la función o método

    def get_cedula(self):  # ejecuta la instrucción correspondiente
        return self.__cedula  # devuelve el resultado desde la función o método

    def get_id(self):  # ejecuta la instrucción correspondiente
        return self.__id  # devuelve el resultado desde la función o método

    def mostrar_info(self):  # define el método para mostrar información
        return f"ID: {self.__id} | Cédula: {self.__cedula} | {self.__nombre} | {self.__correo}"  # devuelve el resultado desde la función o método

    def __str__(self):  # ejecuta la instrucción correspondiente
        return self.mostrar_info()  # devuelve el resultado desde la función o método

    @classmethod  # ejecuta la instrucción correspondiente
    def buscar_por_cedula(cls, cedula):  # ejecuta la instrucción correspondiente
        """Busca si una cédula ya está registrada."""
        return cedula in cls._cedulas_registradas  # devuelve el resultado desde la función o método
