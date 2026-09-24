"""
Módulo de modelos para horarios de atención.
Contiene la clase HorarioAtencion y la función auxiliar formato_12h.
"""

# Importación de módulos necesarios
from datetime import time


# Diccionario que mapea números de día a nombres de días de la semana
# 0 = Lunes, 6 = Domingo
DIAS_SEMANA = {
    0: "Lunes",
    1: "Martes",
    2: "Miercoles",
    3: "Jueves",
    4: "Viernes",
    5: "Sabado",
    6: "Domingo"
}

# convertir formato de 24 horas a 12 horas  ejemplo 14:30 pm a 2:30 pm
def formato_12h(hora_time):
    """
    Convierte una hora en formato 24h a formato 12h con AM/PM.
    
    Args:
        hora_time: Objeto time con la hora en formato 24h.
    
    Returns:
        str: Hora en formato 12h (ej: "1:30 PM", "8:00 AM").
    """
    if hora_time is None:
        return ""
    hora = hora_time.hour
    minutos = hora_time.minute
    if hora == 0:
        return f"12:{minutos:02d} AM"
    elif hora < 12:
        return f"{hora}:{minutos:02d} AM"
    elif hora == 12:
        return f"12:{minutos:02d} PM"
    else:
        return f"{hora - 12}:{minutos:02d} PM"

# clase horario de atencion 
class HorarioAtencion:
    """
    Representa un horario de atención para un día específico de la semana.
    
    Attributes:
        id (int): Identificador único del horario.
        dia_semana (int): Día de la semana (0=Lunes, 6=Domingo).
        hora_inicio (time): Hora de inicio de atención.
        hora_fin (time): Hora de fin de atención.
        hora_inicio_descanso (time): Hora de inicio del descanso (opcional).
        hora_fin_descanso (time): Hora de fin del descanso (opcional).
        activo (bool): Indica si el horario está activo.
    """
    # inicialimzamos el objeto con los atributos que va  a tener 
    def __init__(self, id, dia_semana, hora_inicio, hora_fin, 
                 hora_inicio_descanso=None, hora_fin_descanso=None, activo=True):
        """
        Inicializa un horario de atención.
        
        Args:
            id: Identificador único.
            dia_semana: Día de la semana (0-6).
            hora_inicio: Hora de inicio de atención.
            hora_fin: Hora de fin de atención.
            hora_inicio_descanso: Hora de inicio del descanso (opcional).
            hora_fin_descanso: Hora de fin del descanso (opcional).
            activo: Si el horario está activo (default True).
        """
        self.id = id
        self.dia_semana = dia_semana
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.hora_inicio_descanso = hora_inicio_descanso
        self.hora_fin_descanso = hora_fin_descanso
        self.activo = activo
    
    def __str__(self):
        """Retorna una representación en string del horario."""
        # Obtener nombre del día
        dia_nombre = DIAS_SEMANA.get(self.dia_semana, "Desconocido")
        # Convertir horas a formato 12h
        hora_inicio_12 = formato_12h(self.hora_inicio)# llamamo ala funcion formato 12 para convertir la hora 
        hora_fin_12 = formato_12h(self.hora_fin)# aqui tambien hacemos lo mismo 
        # Construir string de descanso si existe
        descanso = ""
        if self.hora_inicio_descanso and self.hora_fin_descanso:
            
            descanso_inicio = formato_12h(self.hora_inicio_descanso)# aqui tambien 
            descanso_fin = formato_12h(self.hora_fin_descanso) # aqui tambien hacemos lo mismo 
            
            descanso = f" (Descanso {descanso_inicio}-{descanso_fin})"
        return (f"Horario(id={self.id}, {dia_nombre}: {hora_inicio_12}-{hora_fin_12}"
                f"{descanso}, activo={self.activo})")
    
    def tipo(self):
        """Retorna el tipo de objeto."""
        return "HorarioAtencion"
