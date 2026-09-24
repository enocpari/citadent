"""
Módulo de menú de dentistas para la CLI.
Contiene las funciones de interacción con el usuario para CRUD de dentistas.
"""

from backend.models.dentista import Dentista
from cli.input_helpers import input_con_cancelar, confirmar_accion


def agregar_dentista(instancia):
    """Solicita datos y agrega un dentista."""
    print("\n--- Agregar Dentista ---")
    
    name = input_con_cancelar("Ingrese el nombre del dentista")
    if name is None:
        print("Operación cancelada.")
        return
    
    apellido_one = input_con_cancelar("Ingrese el apellido paterno del dentista")
    if apellido_one is None:
        print("Operación cancelada.")
        return
    
    while True:
        phone_str = input_con_cancelar("Ingrese el numero de contacto")
        if phone_str is None:
            print("Operación cancelada.")
            return
        try:
            number_phone = int(phone_str)
            break
        except ValueError:
            print("Error: Debe ingrear un número telefónico válido.")
    
    especialidad = input_con_cancelar("Ingrese la especialidad del dentista")
    if especialidad is None:
        print("Operación cancelada.")
        return
    
    print("\n--- Resumen del Dentista ---")
    print(f"  Nombre: {name} {apellido_one}")
    print(f"  Contacto: {number_phone}")
    print(f"  Especialidad: {especialidad}")
    
    if not confirmar_accion("¿Confirmar agregar dentista?"):
        print("Operación cancelada.")
        return
    
    id = len(instancia.dentistas) + 1
    add_dentista = Dentista(id, name, apellido_one, number_phone, especialidad)
    instancia.agregar_dentista(add_dentista)
    print("Dentista agregado correctamente")


def mostrar_dentistas(instancia):
    """Muestra todos los dentistas."""
    instancia.mostrar_dentistas()


def buscar_dentista_interactivo(instancia):
    """Busca dentista por ID o nombre."""
    input_user = input("Ingrese el id, nombre o apellido del dentista a buscar: ").strip()
    
    if not input_user:
        print(" Error: No ingreso ningun criterio de busqueda")
        return None
    
    if input_user.isdigit():
        dentista = instancia.buscar_dentista(id=int(input_user))
        if dentista:
            print(f" Dentista encontrado por ID: {dentista}")
            return dentista
    
    dentista = instancia.buscar_dentista(nombre=input_user, buscar_parcial=True, devolver_primero=True)
    if dentista:
        print(f" Dentista encontrado: {dentista}")
        return dentista
    
    print(f" No se encontro un dentista con el criterio: '{input_user}'")
    return None
def actualizar_dentista(instancia):
    """Actualiza los datos de un dentista."""
    print("\n--- Actualizar Dentista ---")
    id_str = input_con_cancelar("Ingrese el ID del dentista a actualizar")
    if id_str is None:
        print("Operación cancelada.")
        return
    
    try:
        id = int(id_str)
    except ValueError:
        print("Error: Debe ingrear un número válido.")
        return
    
    dentista_actualizado = instancia.buscar_dentista(id)
    if not dentista_actualizado:
        print("No se encontró un dentista con el ID ingreado.")
        return
    
    print(f"\n--- Datos Actuales ---")
    print(f"  Nombre: {dentista_actualizado.nombre} {dentista_actualizado.apellidopaterno}")
    print(f"  Contacto: {dentista_actualizado.contacto}")
    print(f"  Especialidad: {dentista_actualizado.especialidad}")
    print("\n--- Ingrese los nuevos datos ---")
    
    name = input_con_cancelar("Ingrese el nombre del dentista")
    if name is None:
        print("Operación cancelada.")
        return
    
    apellido_one = input_con_cancelar("Ingrese el apellido paterno del dentista")
    if apellido_one is None:
        print("Operación cancelada.")
        return
    
    while True:
        phone_str = input_con_cancelar("Ingrese el numero de contacto")
        if phone_str is None:
            print("Operación cancelada.")
            return
        try:
            number_phone = int(phone_str)
            break
        except ValueError:
            print("Error: Debe ingrear un número telefónico válido.")
    
    especialidad = input_con_cancelar("Ingrese la especialidad del dentista")
    if especialidad is None:
        print("Operación cancelada.")
        return
    
    print("\n--- Resumen de Cambios ---")
    print(f"  Nombre: {dentista_actualizado.nombre} → {name}")
    print(f"  Apellido: {dentista_actualizado.apellidopaterno} → {apellido_one}")
    print(f"  Contacto: {dentista_actualizado.contacto} → {number_phone}")
    print(f"  Especialidad: {dentista_actualizado.especialidad} → {especialidad}")
    
    if not confirmar_accion("¿Confirmar cambios?"):
        print("Operación cancelada.")
        return
    
    dentista_actualizado.nombre = name
    dentista_actualizado.apellidopaterno = apellido_one
    dentista_actualizado.contacto = number_phone
    dentista_actualizado.especialidad = especialidad
    
    if instancia.actualizar_dentista(id, dentista_actualizado):
        print("Dentista actualizado correctamente")
    else:
        print("No se pudo actualizar el dentista")
def eliminar_dentista(instancia):
    """Elimina un dentista por ID."""
    print("\n--- Eliminar Dentista ---")
    id_str = input_con_cancelar("Ingrese el ID del dentista a eliminar")
    if id_str is None:
        print("Operación cancelada.")
        return
    
    try:
        id = int(id_str)
    except ValueError:
        print("Error: Debe ingrear un número válido.")
        return
    
    dentista = instancia.buscar_dentista(id)
    if not dentista:
        print("No se encontró un dentista con el ID ingreado.")
        return
    
    print(f"\n--- Datos del Dentista ---")
    print(f"  Nombre: {dentista.nombre} {dentista.apellidopaterno}")
    print(f"  Contacto: {dentista.contacto}")
    print(f"  Especialidad: {dentista.especialidad}")
    
    if not confirmar_accion("¿Está seguro de eliminar este dentista?"):
        print("Operación cancelada.")
        return
    
    if instancia.eliminar_dentista(id):
        print("Dentista eliminado correctamente")
    else:
        print("No se encontro un dentista con el id ingresado")


def menu_dentistas(instancia):
    """Menú principal de dentistas."""
    while True:
        print("\n=== Menu Dentistas ===")
        print("1. Agregar dentista")
        print("2. Mostrar dentistas")
        print("3. Buscar dentista")
        print("4. Actualizar dentista")
        print("5. Eliminar dentista")
        print("6. Volver al menu principal")
        opcion = input("Seleccione opcion: ")
        match opcion:
            case "1":
                agregar_dentista(instancia)
            case "2":
                mostrar_dentistas(instancia)
            case "3":
                buscar_dentista_interactivo(instancia)
            case "4":
                actualizar_dentista(instancia)
            case "5":
                eliminar_dentista(instancia)
            case "6":
                break
            case _:
                print("Opcion no valida")