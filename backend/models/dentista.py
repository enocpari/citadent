"""
Módulo de modelo Dentista.
Contiene la clase Dentista que representa a un dentista de la clínica.
"""

# Importación de la clase base Persona
from .persona import Persona


class Dentista(Persona):
    """
    Clase que representa a un dentista de la clínica dental.
    Hereda de la clase Persona y agrega el atributo 'especialidad'.
    
    Attributes:
        id: Identificador único del dentista
        nombre: Nombre de pila
        apellido_paterno: Apellido paterno
        contacto: Número de contacto telefónico
        especialidad: Especialidad del dentista (ej: Ortodoncia, Endodoncia, etc.)
    """
    
    def __init__(self, id, nombre, apellido_paterno, contacto, especialidad):
        """
        Inicializa una instancia de Dentista.
        
        Args: 
            id: Identificador único del dentista
            nombre: Nombre de pila
            apellido_paterno: Apellido paterno
            contacto: Número de contacto telefónico
            especialidad: Especialidad del dentista
        """
        # Llamada al constructor de la clase padre usando argumentos nombrados
        super().__init__(id=id, nombre=nombre, apellido_paterno=apellido_paterno,
                         contacto=contacto)
        # Atributo propio de la clase Dentista
        self.especialidad = especialidad
    

    
    def tipo(self):
        """
        Retorna el tipo de persona.
        
        Returns:
            str: Retorna "Dentista"
        """
        return "Dentista"


