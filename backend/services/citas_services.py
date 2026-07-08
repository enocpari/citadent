"""
Módulo de servicios para gestión de citas.
Contiene la clase citas_services que maneja las operaciones CRUD de citas.
"""

# Importación de modelos y módulos necesarios
from backend.models.cita import Cita
from datetime import datetime, timedelta


class citas_services:
    """
    Clase que gestiona las operaciones de citas en el sistema.
    Almacena las citas en memoria (lista).
    
    Attributes:
        citas: Lista que contiene los objetos Cita registrados.
    """
    
    def __init__(self):
        """Inicializa el servicio de citas con una lista vacía."""
        self.citas = []
    
    def verificar_disponibilidad(self, fecha, hora):
        """
        Verifica si hay una cita pendiente en la fecha y hora especificadas.
        
        Recorre todas las citas existentes y verifica si alguna tiene
        el mismo estado "pendiente" y la misma fecha y hora.
        
        Args:
            fecha: Objeto date con la fecha a verificar.
            hora: Objeto time con la hora a verificar.
        
        Returns:
            bool: True si el horario está disponible, False si ya existe
                  una cita pendiente en ese horario.
        """
        for cita in self.citas:
            if (cita.fecha == fecha and 
                cita.hora == hora and 
                cita.estado == "pendiente"):
                return False
        return True
    
    def agregar_cita(self, cita):
        """
        Agrega una nueva cita al sistema.
        
        Args:
            cita: Objeto Cita a agregar.
        
        Returns:
            bool: True si se agregó, False si el horario está ocupado.
        """
        if not self.verificar_disponibilidad(cita.fecha, cita.hora):
            print("Error: Ya existe una cita en ese horario.")
            return False
        self.citas.append(cita)
        return True
    
    def mostrar_citas(self):
        """Muestra todas las citas registradas en el sistema."""
        if not self.citas:
            print("No hay citas registradas.")
            return
        for cita in self.citas:
            print(cita)
    
    def buscar_cita(self, id):
        """
        Busca una cita por su ID.
        
        Args:
            id: Identificador de la cita a buscar.
        
        Returns:
            Cita o None: La cita encontrada o None si no existe.
        """
        for cita in self.citas:
            if cita.id == id:
                return cita
        return None
    
    def citas_hoy(self):
        """
        Obtiene todas las citas programadas para hoy.
        
        Returns:
            list: Lista de citas con fecha igual a hoy.
        """
        hoy = datetime.now().date()
        return [c for c in self.citas if c.fecha == hoy]
    
    def citas_manana(self):
        """
        Obtiene todas las citas programadas para mañana.
        
        Returns:
            list: Lista de citas con fecha igual a mañana.
        """
        manana = datetime.now().date() + timedelta(days=1)
        return [c for c in self.citas if c.fecha == manana]
    
    def buscar_por_fecha(self, fecha):
        """
        Busca todas las citas de una fecha específica.
        
        Args:
            fecha: Objeto date con la fecha a buscar.
        
        Returns:
            list: Lista de citas en esa fecha.
        """
        return [c for c in self.citas if c.fecha == fecha]
    
    def actualizar_fecha_hora(self, id, fecha, hora):
        """
        Actualiza la fecha y hora de una cita existente.
        
        Args:
            id: ID de la cita a actualizar.
            fecha: Nueva fecha (objeto date).
            hora: Nueva hora (objeto time).
        
        Returns:
            bool: True si se actualizó, False si no se encontró.
        """
        for cita in self.citas:
            if cita.id == id:
                cita.fecha = fecha
                cita.hora = hora
                return True
        return False
    
    def completar_cita(self, id):
        """
        Marca una cita como completada.
        
        Args:
            id: ID de la cita a completar.
        
        Returns:
            bool: True si se completó, False si no existe o no está pendiente.
        """
        for cita in self.citas:
            if cita.id == id:
                if cita.estado == "pendiente":
                    cita.estado = "completada"
                    return True
                else:
                    print(f"La cita no está pendiente, actualmente está: {cita.estado}")
                    return False
        return False
    
    def cancelar_cita(self, id):
        """
        Cancela una cita existente.
        
        Args:
            id: ID de la cita a cancelar.
        
        Returns:
            bool: True si se canceló, False si no existe o no está pendiente.
        """
        for cita in self.citas:
            if cita.id == id:
                if cita.estado == "pendiente":
                    cita.estado = "cancelada"
                    return True
                else:
                    print(f"La cita no está pendiente, actualmente está: {cita.estado}")
                    return False
        return False
    
    def eliminar_cita(self, id):
        """
        Elimina una cita del sistema.
        
        Args:
            id: ID de la cita a eliminar.
        
        Returns:
            bool: True si se eliminó, False si no se encontró.
        """
        for cita in self.citas:
            if cita.id == id:
                self.citas.remove(cita)
                return True
        return False
    
    def buscar_por_paciente(self, nombre=None, apellido=None, contacto=None):
        """
        Busca citas por datos del paciente.
        
        Args:
            nombre: Nombre del paciente (opcional).
            apellido: Apellido del paciente (opcional).
            contacto: Teléfono del paciente (opcional).
        
        Returns:
            list: Lista de citas que coinciden con los criterios.
        """
        resultados = []
        for cita in self.citas:
            match = True
            if nombre:
                if nombre.lower() not in cita.nombre.lower():
                    match = False
            if apellido and match:
                if (apellido.lower() not in cita.apellido_paterno.lower() and 
                    apellido.lower() not in cita.apellido_materno.lower()):
                    match = False
            if contacto and match:
                if contacto not in str(cita.contacto):
                    match = False
            if match:
                resultados.append(cita)
        return resultados
    
    def get_citas_por_estado(self, estado):
        """
        Obtiene todas las citas con un estado específico.
        
        Args:
            estado: Estado a filtrar ("pendiente", "completada", "cancelada").
        
        Returns:
            list: Lista de citas con el estado especificado.
        """
        return [c for c in self.citas if c.estado == estado]
    
    def get_citas_completadas(self):
        """
        Obtiene todas las citas completadas.
        
        Returns:
            list: Lista de citas con estado "completada".
        """
        return self.get_citas_por_estado("completada")
    
    def get_citas_canceladas(self):
        """
        Obtiene todas las citas canceladas.
        
        Returns:
            list: Lista de citas con estado "cancelada".
        """
        return self.get_citas_por_estado("cancelada")
    
    def get_citas_pendientes(self):
        """
        Obtiene todas las citas pendientes.
        
        Returns:
            list: Lista de citas con estado "pendiente".
        """
        return self.get_citas_por_estado("pendiente")
    
    def get_citas_por_fecha_y_estado(self, fecha, estado):
        """
        Obtiene citas de una fecha específica con estado específico.
        
        Args:
            fecha: Objeto date con la fecha a buscar.
            estado: Estado de la cita a filtrar.
        
        Returns:
            list: Lista de citas que coinciden con fecha y estado.
        """
        return [c for c in self.citas if c.fecha == fecha and c.estado == estado]
    
    def get_citas_por_mes_y_estado(self, year, month, estado):
        """
        Obtiene citas de un mes específico con estado específico.
        
        Args:
            year: Año de la búsqueda.
            month: Mes de la búsqueda (1-12).
            estado: Estado de la cita a filtrar.
        
        Returns:
            list: Lista de citas que coinciden con mes, año y estado.
        """
        return [c for c in self.citas 
                if c.fecha.year == year and c.fecha.month == month and c.estado == estado]
