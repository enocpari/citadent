"""
Módulo de servicios para gestión de dentistas.
Contiene la clase dentista_services que maneja las operaciones CRUD de dentistas.
"""

# Importación del modelo Dentista
from backend.models.dentista import Dentista


class dentista_services:
    """
    Clase que gestiona las operaciones de dentistas en el sistema.
    Almacena los dentistas en memoria (lista).
    
    Attributes:
        dentistas: Lista que contiene los objetos Dentista registrados.
    """
    
    def __init__(self):
        """Inicializa el servicio de dentistas con una lista vacía."""
        self.dentistas = []
    
    def agregar_dentista(self, dentista):
        """
        Agrega un dentista a la lista de dentistas.
        
        Args:
            dentista: Objeto Dentista a agregar.
        """
        self.dentistas.append(dentista)
    
    def eliminar_dentista(self, id):
        """
        Elimina un dentista de la lista por su ID.
        
        Args:
            id: Identificador del dentista a eliminar.
        
        Returns:
            bool: True si se eliminó, False si no se encontró.
        """
        if not self.dentistas:
            print("No hay dentistas registrados que eliminar.")
            return False
        
        for dentista in self.dentistas:
            if dentista.id == id:
                del self.dentistas[self.dentistas.index(dentista)]
                return True
        return False
    
    def mostrar_dentistas(self):
        """Muestra todos los dentistas registrados en el sistema."""
        if not self.dentistas:
            print("No hay dentistas registrados.")
            return
        
        for dentista in self.dentistas:
            print(dentista)
    
    def buscar_dentista(self, id=None, nombre=None, buscar_parcial=False, devolver_primero=False):
        """
        Busca dentistas por diferentes criterios.
        
        Args:
            id: ID exacto del dentista (opcional).
            nombre: Nombre del dentista (opcional).
            buscar_parcial: Si True, busca coincidencias parciales.
            devolver_primero: Si True, retorna solo el primer resultado.
        
        Returns:
            Dentista, list o None: Según los parámetros de búsqueda.
        """
        resultados = []
        
        for dentista in self.dentistas:
            # Buscar por ID
            if id is not None and dentista.id == id:
                return dentista
            
            # Buscar por nombre
            if nombre is not None:
                if buscar_parcial:
                    if (nombre.lower() in dentista.nombre.lower() or 
                        nombre.lower() in dentista.apellidopaterno.lower()):
                        resultados.append(dentista)
                else:
                    if (dentista.nombre.lower() == nombre.lower() or 
                        dentista.apellidopaterno.lower() == nombre.lower()):
                        return dentista
        
        if devolver_primero and resultados:
            return resultados[0]
        
        return resultados if resultados else None
    
    def actualizar_dentista(self, id, datos_actualizados):
        """
        Actualiza los datos de un dentista existente.
        
        Args:
            id: ID del dentista a actualizar.
            datos_actualizados: Objeto Dentista con los nuevos datos.
        
        Returns:
            bool: True si se actualizó, False si no se encontró.
        """
        for dentista in self.dentistas:
            if dentista.id == id:
                if datos_actualizados.nombre:
                    dentista.nombre = datos_actualizados.nombre
                if datos_actualizados.apellidopaterno:
                    dentista.apellidopaterno = datos_actualizados.apellidopaterno
                if datos_actualizados.contacto:
                    dentista.contacto = datos_actualizados.contacto
                if datos_actualizados.especialidad:
                    dentista.especialidad = datos_actualizados.especialidad
                return True
        return False
            
