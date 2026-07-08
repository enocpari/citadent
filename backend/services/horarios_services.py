from backend.models.horario_atencion import HorarioAtencion, DIAS_SEMANA


class horarios_services:
    """
    Servicio para gestionar los horarios de atencion de la clinica.
    
    Permite agregar, mostrar, buscar y eliminar horarios de atencion,
    asi como verificar si una fecha y hora esta dentro del horario valido.
    """
    
    def __init__(self):
        """Inicializa el servicio con una lista vacia de horarios."""
        self.horarios = []
    
    def agregar_horario(self, horario):
        """
        Agrega un nuevo horario de atencion.
        
        Args:
            horario: Objeto HorarioAtencion a agregar.
        
        Returns:
            bool: True si se agrego exitosamente.
        """
        self.horarios.append(horario)
        return True
    
    def mostrar_horarios(self):
        """
        Muestra todos los horarios de atencion registrados.
        
        Si no hay horarios, muestra un mensaje informativo.
        """
        if not self.horarios:
            print("No hay horarios de atencion registrados.")
            return
        for horario in self.horarios:
            print(horario)
    
    def buscar_horario_por_dia(self, dia_semana):
        """
        Busca un horario de atencion para un dia especifico.
        
        Args:
            dia_semana: Numero del dia de la semana (0-6).
        
        Returns:
            HorarioAtencion: El horario encontrado o None.
        """
        for horario in self.horarios:
            if horario.dia_semana == dia_semana:
                return horario
        return None
    
    def buscar_horario_por_id(self, id):
        """
        Busca un horario de atencion por su ID.
        
        Args:
            id: Identificador del horario.
        
        Returns:
            HorarioAtencion: El horario encontrado o None.
        """
        for horario in self.horarios:
            if horario.id == id:
                return horario
        return None
    
    def eliminar_horario(self, id):
        """
        Elimina un horario de atencion por su ID.
        
        Args:
            id: Identificador del horario a eliminar.
        
        Returns:
            bool: True si se elimino exitosamente, False si no se encontro.
        """
        for horario in self.horarios:
            if horario.id == id:
                self.horarios.remove(horario)
                return True
        return False
    
    def get_horario_para_dia(self, fecha):
        """
        Obtiene el horario de atencion para una fecha especifica.
        
        Args:
            fecha: Objeto date con la fecha a verificar.
        
        Returns:
            HorarioAtencion: El horario para ese dia o None si no existe.
        """
        dia_semana = fecha.weekday()  # 0=Lunes, 6=Domingo
        return self.buscar_horario_por_dia(dia_semana)
    
    def verificar_horario_atencion(self, fecha, hora):
        """
        Verifica si la fecha y hora estan dentro del horario de atencion
        y fuera del horario de descanso.
        
        Args:
            fecha: Objeto date con la fecha a verificar.
            hora: Objeto time con la hora a verificar.
        
        Returns:
            tuple: (bool, str) - (True si es valido, mensaje descriptivo)
        """
        horario = self.get_horario_para_dia(fecha)
        
        # Verificar si existe horario para ese dia
        if not horario:
            dia_nombre = DIAS_SEMANA.get(fecha.weekday(), "Desconocido")
            return (False, f"No hay atencion los {dia_nombre}")
        
        # Verificar si el horario esta activo
        if not horario.activo:
            dia_nombre = DIAS_SEMANA.get(fecha.weekday(), "Desconocido")
            return (False, f"No hay atencion los {dia_nombre}")
        
        # Verificar rango de atencion
        if not (horario.hora_inicio <= hora <= horario.hora_fin):
            return (False, f"Horario fuera de atencion. Debe ser entre {horario.hora_inicio} y {horario.hora_fin}")
        
        # Verificar horario de descanso
        if horario.hora_inicio_descanso and horario.hora_fin_descanso:
            if horario.hora_inicio_descanso <= hora <= horario.hora_fin_descanso:
                return (False, f"Horario de descanso ({horario.hora_inicio_descanso} - {horario.hora_fin_descanso}). Elija otro horario.")
        
        return (True, "Horario valido")
    
    def hay_horarios_configurados(self):
        """
        Verifica si hay horarios de atencion configurados.
        
        Returns:
            bool: True si hay al menos un horario configurado.
        """
        return len(self.horarios) > 0
