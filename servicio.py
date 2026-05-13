from entidad import Entidad  # importa la clase o excepción necesaria
from excepciones import ServicioError  # importa la clase o excepción necesaria


class Servicio(Entidad):  # declara la clase

    def __init__(self, nombre, precio_base):  # define el constructor de la clase
        self.__nombre = nombre  # asigna un valor a una variable o atributo
        self.__precio_base = precio_base  # asigna un valor a una variable o atributo
        self.validar()  # ejecuta la instrucción correspondiente

    @property  # ejecuta la instrucción correspondiente
    def nombre(self):  # ejecuta la instrucción correspondiente
        return self.__nombre  # devuelve el resultado desde la función o método

    @property  # ejecuta la instrucción correspondiente
    def precio_base(self):  # ejecuta la instrucción correspondiente
        return self.__precio_base  # devuelve el resultado desde la función o método

    def validar(self):  # define el método validar de la clase
        if not isinstance(self.__nombre, str) or not self.__nombre.strip():  # verifica que el valor sea del tipo esperado
            raise ServicioError("El nombre del servicio es obligatorio")  # lanza una excepción cuando ocurre un error

        if not isinstance(self.__precio_base, (int, float)) or self.__precio_base <= 0:  # verifica que el valor sea del tipo esperado
            raise ServicioError("El precio base del servicio debe ser mayor a cero")  # lanza una excepción cuando ocurre un error

    def mostrar_info(self):  # define el método para mostrar información
        return f"{self.nombre} - ${self.precio_base:,.0f}"  # devuelve el resultado desde la función o método

    def calcular_costo(self, impuesto=0, descuento=0):  # define el método para calcular el costo
        raise ServicioError("El servicio no implementa el cálculo de costo")  # lanza una excepción cuando ocurre un error

    def describir_servicio(self):  # define el método para describir el servicio
        raise ServicioError("El servicio no implementa descripción")  # lanza una excepción cuando ocurre un error


class ReservaSala(Servicio):  # declara la clase

    def __init__(self, nombre, precio_base, horas):  # define el constructor de la clase
        self.horas = horas  # asigna un valor a una variable o atributo
        super().__init__(nombre, precio_base)  # ejecuta la instrucción correspondiente
        self.validar()  # ejecuta la instrucción correspondiente

    def validar(self):  # define el método validar de la clase
        super().validar()  # ejecuta la instrucción correspondiente
        if not isinstance(self.horas, int) or self.horas <= 0:  # verifica que el valor sea del tipo esperado
            raise ServicioError("La duración de la reserva debe ser un número de horas mayor a cero")  # lanza una excepción cuando ocurre un error

    def calcular_costo(self, impuesto=0, descuento=0):  # define el método para calcular el costo
        total = self.precio_base * self.horas  # asigna un valor a una variable o atributo
        if impuesto < 0 or descuento < 0:  # evalúa una condición para decidir el flujo
            raise ServicioError("Impuesto y descuento deben ser valores no negativos")  # lanza una excepción cuando ocurre un error
        total += total * impuesto  # asigna un valor a una variable o atributo
        total -= descuento  # asigna un valor a una variable o atributo
        return total  # devuelve el resultado desde la función o método

    def describir_servicio(self):  # define el método para describir el servicio
        return f"Reserva de sala por {self.horas} horas"  # devuelve el resultado desde la función o método


class AlquilerEquipo(Servicio):  # declara la clase

    def __init__(self, nombre, precio_base, dias):  # define el constructor de la clase
        self.dias = dias  # asigna un valor a una variable o atributo
        super().__init__(nombre, precio_base)  # ejecuta la instrucción correspondiente
        self.validar()  # ejecuta la instrucción correspondiente

    def validar(self):  # define el método validar de la clase
        super().validar()  # ejecuta la instrucción correspondiente
        if not isinstance(self.dias, int) or self.dias <= 0:  # verifica que el valor sea del tipo esperado
            raise ServicioError("Los días de alquiler deben ser un número entero mayor a cero")  # lanza una excepción cuando ocurre un error

    def calcular_costo(self, impuesto=0, descuento=0):  # define el método para calcular el costo
        total = self.precio_base * self.dias  # asigna un valor a una variable o atributo
        if impuesto < 0 or descuento < 0:  # evalúa una condición para decidir el flujo
            raise ServicioError("Impuesto y descuento deben ser valores no negativos")  # lanza una excepción cuando ocurre un error
        return total + total * impuesto - descuento  # devuelve el resultado desde la función o método

    def describir_servicio(self):  # define el método para describir el servicio
        return f"Alquiler de equipo por {self.dias} días"  # devuelve el resultado desde la función o método


class AsesoriaEspecializada(Servicio):  # declara la clase

    def __init__(self, nombre, precio_base, horas, especialista):  # define el constructor de la clase
        self.horas = horas  # asigna un valor a una variable o atributo
        self.especialista = especialista  # asigna un valor a una variable o atributo
        super().__init__(nombre, precio_base)  # ejecuta la instrucción correspondiente
        self.validar()  # ejecuta la instrucción correspondiente

    def validar(self):  # define el método validar de la clase
        super().validar()  # ejecuta la instrucción correspondiente
        if not isinstance(self.horas, int) or self.horas <= 0:  # verifica que el valor sea del tipo esperado
            raise ServicioError("La duración de la asesoría debe ser un número de horas mayor a cero")  # lanza una excepción cuando ocurre un error
        if not isinstance(self.especialista, str) or not self.especialista.strip():  # verifica que el valor sea del tipo esperado
            raise ServicioError("El especialista debe ser un nombre válido")  # lanza una excepción cuando ocurre un error

    def calcular_costo(self, impuesto=0, descuento=0):  # define el método para calcular el costo
        total = self.precio_base * self.horas  # asigna un valor a una variable o atributo
        if impuesto < 0 or descuento < 0:  # evalúa una condición para decidir el flujo
            raise ServicioError("Impuesto y descuento deben ser valores no negativos")  # lanza una excepción cuando ocurre un error
        return total + total * impuesto - descuento  # devuelve el resultado desde la función o método

    def describir_servicio(self):  # define el método para describir el servicio
        return f"Asesoría especializada con {self.especialista} por {self.horas} horas"  # devuelve el resultado desde la función o método
