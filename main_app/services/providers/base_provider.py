# main_app/services/providers/base_provider.py

from abc import ABC, abstractmethod

class Provider(ABC):
    @abstractmethod
    def fetch_profiles(self):
        """
        Método para obtener perfiles de escorts de la fuente de datos.
        Debe ser implementado por cada proveedor.
        """
        pass
