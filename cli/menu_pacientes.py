"""
Módulo de menú de pacientes para la CLI.
Contiene las funciones de interacción con el usuario para CRUD de pacientes.
"""

from backend.models.paciente import Paciente
from cli.input_helpers import input_con_cancelar, confirmar_accion


def agregar_paciente(instancia):
    """Solicita datos y agrega un paciente."""
    print("\n--- Agregar Paciente ---")
    
    name = input_con_cancelar("Ingrese el nombre del paciente")
    if name is None:
        print("Operación cancelada.")
        return
    
    apellido_one = input_con_cancelar("Ingrese el apellido paterno del paciente")
    if apellido_one is None:
        print("Operación cancelada.")
        return
    
    apellido_second = input_con_cancelar("Ingrese el apellido materno del paciente")
    if apellido_second is None:
        print("Operación cancelada.")
        return
    
    while True:
        age_str = input_con_cancelar("Ingrese la edad del paciente")
        if age_str is None:
            print("Operación cancelada.")
            return
        try:
            age = int(age_str)
            break
        except ValueError:
            print("Error: Debe ingresar un número válido.")
    
    while True:
        gener_input = input_con_cancelar("Ingrese x para masculino")
        if gener_input is None:
            print("Operación cancelada.")
            return
        gener = "masculino" if gener_input == "x" else "femenino"
        break
    
    while True:
        phone_str = input_con_cancelar("Ingrese el numero de contacto")
        if phone_str is None:
            print("Operación cancelada.")
            return
        try:
            number_phone = int(phone_str)
            break
        except ValueError:
            print("Error: Debe ingresar un número telefónico válido.")
    
    print("\n--- Resumen del Paciente ---")
    print(f"  Nombre: {name} {apellido_one} {apellido_second}")
    print(f"  Edad: {age}")
    print(f"  Género: {gener}")
    print(f"  Contacto: {number_phone}")
    
    if not confirmar_accion("¿Confirmar agregar paciente?"):
        print("Operación cancelada.")
        return
    
    id = len(instancia.pacientes) + 1
    add_paciente = Paciente(id, name, apellido_one, apellido_second, age, gener, number_phone)
    instancia.agregar_paciente(add_paciente)
    print("Paciente agregado correctamente")


def buscar_paciente_interactivo(instancia):
    """Busca paciente por ID, nombre o apellido de forma interactiva."""
    input_user = input("Ingrese el id, nombre o apellido del paciente a buscar: ").strip()
    
    if not input_user:
        print(" Error: No ingreso ningun criterio de busqueda")
        return None
    
    if input_user.isdigit():
        paciente = instancia.buscar_paciente(id=int(input_user), devolver_primero=True)
        if paciente:
            print(f" Paciente encontrado por ID: {paciente}")
            return paciente
    
    paciente = instancia.buscar_paciente(nombre=input_user, buscar_parcial=True, devolver_primero=True)
    if paciente:
        print(f" Paciente encontrado por nombre: {paciente}")
        return paciente
    
    paciente = instancia.buscar_paciente(apellido=input_user, buscar_parcial=True, devolver_primero=True)
    if paciente:
        print(f" Paciente encontrado por apellido: {paciente}")
        return paciente
    
    print(f" No se encontro un paciente con el criterio: '{input_user}'")
    return None


def eliminar_paciente(instancia):
    """Elimina un paciente por ID."""
    print("\n--- Eliminar Paciente ---")
    id_str = input_con_cancelar("Ingrese el ID del paciente a eliminar")
    if id_str is None:
        print("Operación cancelada.")
        return
    
    try:
        id = int(id_str)
    except ValueError:
        print("Error: Debe ingresar un número válido.")
        return
    
    paciente = instancia.buscar_paciente(id)
    if not paciente:
        print("No se encontró un paciente con el ID ingresaado.")
        return
    
    print(f"\n--- Datos del Paciente ---")
    print(f"  Nombre: {paciente.nombre} {paciente.apellidopaterno} {paciente.apellidomaterno}")
    print(f"  Edad: {paciente.edad}")
    print(f"  Género: {paciente.genero}")
    print(f"  Contacto: {paciente.contacto}")
    
    if not confirmar_accion("¿Está seguro de eliminar este paciente?"):
        print("Operación cancelada.")
        return
    
    if instancia.eliminar_paciente(id):
        print("Paciente eliminado correctamente")
    else:
        print("No se pudo eliminar el paciente.")
def actualizar_paciente(instancia):
    """Actualiza los datos de un paciente."""
    print("\n--- Actualizar Paciente ---")
    id_str = input_con_cancelar("Ingrese el ID del paciente a actualizar")
    if id_str is None:
        print("Operación cancelada.")
        return
    
    try:
        id = int(id_str)
    except ValueError:
        print("Error: Debe ingrear un número válido.")
        return
    
    paciente_actualizado = instancia.buscar_paciente(id)
    if not paciente_actualizado:
        print("No se encontró un paciente con el ID ingreado.")
        return
    
    print(f"\n--- Datos Actuales ---")
    print(f"  Nombre: {paciente_actualizado.nombre} {paciente_actualizado.apellidopaterno} {paciente_actualizado.apellidomaterno}")
    print(f"  Edad: {paciente_actualizado.edad}")
    print(f"  Género: {paciente_actualizado.genero}")
    print(f"  Contacto: {paciente_actualizado.contacto}")
    print("\n--- Ingrese los nuevos datos ---")
    
    name = input_con_cancelar("Ingrese el nombre del paciente")
    if name is None:
        print("Operación cancelada.")
        return
    
    apellido_one = input_con_cancelar("Ingrese el apellido paterno del paciente")
    if apellido_one is None:
        print("Operación cancelada.")
        return
    
    apellido_second = input_con_cancelar("Ingrese el apellido materno del paciente")
    if apellido_second is None:
        print("Operación cancelada.")
        return
    
    while True:
        age_str = input_con_cancelar("Ingrese la edad del paciente")
        if age_str is None:
            print("Operación cancelada.")
            return
        try:
            age = int(age_str)
            break
        except ValueError:
            print("Error: Debe ingrear un número válido.")
    
    while True:
        gener_input = input_con_cancelar("Ingrese x para masculino")
        if gener_input is None:
            print("Operación cancelada.")
            return
        gener = "masculino" if gener_input == "x" else "femenino"
        break
    
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
    
    print("\n--- Resumen de Cambios ---")
    print(f"  Nombre: {paciente_actualizado.nombre} → {name}")
    print(f"  Apellido Paterno: {paciente_actualizado.apellidopaterno} → {apellido_one}")
    print(f"  Apellido Materno: {paciente_actualizado.apellidomaterno} → {apellido_second}")
    print(f"  Edad: {paciente_actualizado.edad} → {age}")
    print(f"  Género: {paciente_actualizado.genero} → {gener}")
    print(f"  Contacto: {paciente_actualizado.contacto} → {number_phone}")
    
    if not confirmar_accion("¿Confirmar cambios?"):
        print("Operación cancelada.")
        return
    
    paciente_actualizado.nombre = name
    paciente_actualizado.apellidopaterno = apellido_one
    paciente_actualizado.apellidomaterno = apellido_second
    paciente_actualizado.edad = age
    paciente_actualizado.genero = gener
    paciente_actualizado.contacto = number_phone
    
    if instancia.actualizar_paciente(id, paciente_actualizado):
        print("Paciente actualizado correctamente")
    else:
        print("No se pudo actualizar el paciente")


def menu_pacientes(instancia):
    """Menú principal de pacientes."""
    while True:
        print("\n=== Menu Pacientes ===")
        print("1. Agregar paciente")
        print("2. Mostrar pacientes")
        print("3. Buscar paciente")
        print("4. Actualizar paciente")
        print("5. Eliminar paciente")
        print("6. Volver al menu principal")
        opcion = input("Seleccione opcion: ")
        match opcion:
            case "1":
                agregar_paciente(instancia)
            case "2":
                mostrar_pacientes(instancia)
            case "3":
                buscar_paciente_interactivo(instancia)
            case "4":
                actualizar_paciente(instancia)
            case "5":
                eliminar_paciente(instancia)
            case "6":
                break
            case _:
                print("Opcion no valida")