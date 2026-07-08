"""
Módulo de modelo Paciente.
Contiene la clase Paciente que representa a un paciente de la clínica dental.
"""

# Importación de la clase base Persona
from .persona import Persona


class Paciente(Persona):
    """
    Clase que representa a un paciente de la clínica dental.
    Hereda de la clase Persona.
    
    Attributes:
        id: Identificador único del paciente
        nombre: Nombre de pila
        apellido_paterno: Apellido paterno
        apellido_materno: Apellido materno
        edad: Edad del paciente
        genero: Género del paciente
        contacto: Número de contacto telefónico
    """
    
    def __init__(self, id, nombre, apellido_paterno, apellido_materno, 
                 edad, genero, contacto):
        """
        Inicializa una instancia de Paciente.
        
        Args:
            id: Identificador único del paciente
            nombre: Nombre de pila
            apellido_paterno: Apellido paterno
            apellido_materno: Apellido materno
            edad: Edad del paciente
            genero: Género del paciente
            contacto: Número de contacto telefónico
        """
        # Llamada al constructor de la clase padre (Persona)
        super().__init__(id, nombre, apellido_paterno, apellido_materno, 
                         edad, genero, contacto)
    
    def __str__(self):
        """
        Retorna una representación en string del paciente.
        
        Returns:
            str: Información formateada del paciente
        """
        return (f"Paciente id:{self.id}( nombre:'{self.nombre}', "
                f"apellidos:'{self.apellido_paterno} {self.apellido_materno}', "
                f"edad:{self.edad}, sexo:'{self.genero}', contacto: +591-{self.contacto})")
    
    def tipo(self):
        """
        Retorna el tipo de persona.
        
        Returns:
            str: Retorna "Paciente"
        """
        return "Paciente"
    

