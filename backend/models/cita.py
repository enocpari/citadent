"""
Módulo de modelo Cita.
Contiene la clase Cita que representa una cita médica en el sistema.
"""

# Importaciones de módulos necesarios
from datetime import date, time
# Importación de función auxiliar para convertir hora a formato 12h
from backend.models.horario_atencion import formato_12h
           
class Cita:
    """
    Clase que representa una cita médica en la clínica dental.
    
    Attributes:
        id: Identificador único de la cita
        nombre: Nombre del paciente
        apellido_paterno: Apellido paterno del paciente
        apellido_materno: Apellido materno del paciente
        contacto: Número de contacto del paciente
        fecha: Fecha de la cita (objeto date)
        hora: Hora de la cita (objeto time)
        estado: Estado de la cita ("pendiente", "completada", "cancelada")
    """
    
    def __init__(self, id, nombre, apellido_paterno, apellido_materno, 
                 contacto, fecha, hora, estado="pendiente"):
        """
        Inicializa una instancia de Cita.
        
        Args:
            id: Identificador único de la cita
            nombre: Nombre del paciente
            apellido_paterno: Apellido paterno del paciente
            apellido_materno: Apellido materno del paciente
            contacto: Número de contacto del paciente
            fecha: Fecha de la cita (objeto date)
            hora: Hora de la cita (objeto time)
            estado: Estado de la cita (por defecto "pendiente")
        """
        self.id = id
        self.nombre = nombre
        self.apellido_paterno = apellido_paterno
        self.apellido_materno = apellido_materno
        self.contacto = contacto
        self.fecha = fecha
        self.hora = hora
        self.estado = estado
    
    def __str__(self):
        """
        Retorna una representación en string de la cita.
        
        Returns:
            str: Información formateada de la cita con hora en formato 12h
        """
        # Convertir hora a formato 12h (ej: 2:00 PM)
        hora_12 = formato_12h(self.hora)
        # Concatenar nombre completo del paciente
        nombre_completo = f"{self.nombre} {self.apellido_paterno} {self.apellido_materno}"
        return (f"Cita(id={self.id}, paciente:'{nombre_completo}', "
                f"fecha:{self.fecha}, hora:{hora_12}, estado:{self.estado}, "
                f"contacto:+591-{self.contacto})")
    
    def tipo(self):
        """
        Retorna el tipo de objeto.
        
        Returns:
            str: Retorna "Cita"
        """
        return "Cita"
