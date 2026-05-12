from abc import ABC, abstractmethod


class Entidad(ABC):
    @abstractmethod
    def validar(self):
        """Valida los datos internos de la entidad."""
        pass

    @abstractmethod
    def mostrar_info(self):
        """Devuelve un texto representativo de la entidad."""
        pass
