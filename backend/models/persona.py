"""
Módulo de modelos base para personas.
Contiene la clase abstracta Persona que serve como base para pacientes y dentistas.
"""

# Importación de módulos necesarios para abstracción
from abc import ABC, abstractmethod
from typing import Optional


class Persona(ABC):
    """
    Clase abstracta que representa una persona en el sistema.
    Serve como clase base para Paciente y Dentista.
    
    Attributes:
        id: Identificador único de la persona
        nombre: Nombre de pila de la persona
        apellido_paterno: Apellido paterno
        apellido_materno: Apellido materno (opcional)
        edad: Edad de la persona (opcional)
        genero: Género de la persona (opcional)
        contacto: Número de contacto (opcional)
    """
    
    def __init__(self, id: int, nombre: str, apellido_paterno: str, 
                 apellido_materno: Optional[str] = None, 
                 edad: Optional[int] = None, 
                 genero: Optional[str] = None, 
                 contacto: Optional[str] = None):
        """
        Inicializa una instancia de Persona.
        
        Args:
            id: Identificador único
            nombre: Nombre de pila
            apellido_paterno: Apellido paterno
            apellido_materno: Apellido materno (opcional)
            edad: Edad (opcional)
            genero: Género (opcional)
            contacto: Número de contacto (opcional)
        """
        self.id = id
        self.nombre = nombre
        self.apellido_paterno = apellido_paterno
        self.apellido_materno = apellido_materno
        self.edad = edad
        self.genero = genero
        self.contacto = contacto
    # que es el metodo abstracto.AI!
    @abstractmethod
    def __str__(self) -> str:
        """Método abstracto para representación en string"""
        pass
    
    @abstractmethod
    def tipo(self) -> str:
        """Método abstracto que retorna el tipo de persona"""
        pass
