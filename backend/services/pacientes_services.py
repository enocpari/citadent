"""
Módulo de servicios para gestión de pacientes.
Contiene la clase pacientes_services que maneja las operaciones CRUD de pacientes.
"""

# Importación del modelo Paciente
from backend.models.paciente import Paciente


class pacientes_services:
    """
    Clase que gestiona las operaciones de pacientes en el sistema.
    Almacena los pacientes en memoria (lista).
    
    Attributes:
        pacientes: Lista que contiene los objetos Paciente registrados.
    """
    
    def __init__(self):
        """Inicializa el servicio de pacientes con una lista vacía."""
        self.pacientes = []
    
    def agregar_paciente(self, paciente):
        """
        Agrega un paciente a la lista de pacientes.
        
        Args:
            paciente: Objeto Paciente a agregar.
        """
        self.pacientes.append(paciente)
    
    def eliminar_paciente(self, id):
        """
        Elimina un paciente de la lista por su ID.
        
        Args:
            id: Identificador del paciente a eliminar.
        
        Returns:
            bool: True si se eliminó, False si no se encontró.
        """
        if not self.pacientes:
            print("No hay pacientes registrados que eliminar.")
            return False
        
        for paciente in self.pacientes:
            if paciente.id == id:
                del self.pacientes[self.pacientes.index(paciente)]
                return True
        return False
    
    def mostrar_pacientes(self):
        """Muestra todos los pacientes registrados en el sistema."""
        if not self.pacientes:
            print("No hay pacientes registrados.")
            return
        
        for paciente in self.pacientes:
            print(paciente)
    
    def buscar_paciente(self, id=None, nombre=None, apellido=None, 
                        buscar_parcial=False, devolver_primero=False):
        """
        Busca pacientes por diferentes criterios.
        
        Args:
            id: ID exacto del paciente (opcional).
            nombre: Nombre del paciente (opcional).
            apellido: Apellido del paciente (opcional).
            buscar_parcial: Si True, busca coincidencias parciales.
            devolver_primero: Si True, retorna solo el primer resultado.
        
        Returns:
            Paciente, list o None: Según los parámetros de búsqueda.
        """
        resultados = []
        
        for paciente in self.pacientes:
            coincide = True
            
            # Verificar ID
            if id is not None and paciente.id != id:
                coincide = False
            
            # Verificar nombre
            if nombre is not None and coincide:
                nombre_buscar = nombre.lower() if buscar_parcial else nombre
                
                if buscar_parcial:
                    if nombre_buscar not in paciente.nombre.lower():
                        coincide = False
                else:
                    if paciente.nombre != nombre:
                        coincide = False
            
            # Verificar apellido (busca en paterno y materno)
            if apellido is not None and coincide:
                apellido_buscar = apellido.lower() if buscar_parcial else apellido
                
                # Normalizar apellidos para comparación
                apellido_paterno = paciente.apellidopaterno
                apellido_materno = paciente.apellidomaterno
                apellido_completo = f"{apellido_paterno} {apellido_materno}"
                
                if buscar_parcial:
                    # Búsqueda parcial en cualquiera de los apellidos
                    if (apellido_buscar not in apellido_paterno.lower() and 
                        apellido_buscar not in apellido_materno.lower() and
                        apellido_buscar not in apellido_completo.lower()):
                        coincide = False
                else:
                    # Búsqueda exacta: puede coincidir con paterno, materno o completo
                    if (apellido_paterno != apellido and 
                        apellido_materno != apellido and
                        apellido_completo != apellido):
                        coincide = False
        
            if coincide:
                resultados.append(paciente)
                if devolver_primero:
                    return paciente
    
        return resultados if resultados else None
    
    def actualizar_paciente(self, id, paciente_actualizado):
        """
        Actualiza los datos de un paciente existente.
        
        Args:
            id: ID del paciente a actualizar.
            paciente_actualizado: Objeto Paciente con los nuevos datos.
        
        Returns:
            bool: True si se actualizó, False si no se encontró.
        """
        for i, paciente in enumerate(self.pacientes):
            if paciente.id == id:
                self.pacientes[i] = paciente_actualizado
                return True
        return False
    

