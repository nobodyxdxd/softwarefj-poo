from abc import ABC, abstractmethod  # importa la clase o excepción necesaria


class Entidad(ABC):  # declara la clase
    @abstractmethod  # ejecuta la instrucción correspondiente
    def validar(self):  # define el método validar de la clase
        """Valida los datos internos de la entidad."""
        pass  # no hace nada; placeholder para el método abstracto

    @abstractmethod  # ejecuta la instrucción correspondiente
    def mostrar_info(self):  # define el método para mostrar información
        """Devuelve un texto representativo de la entidad."""
        pass  # no hace nada; placeholder para el método abstracto
