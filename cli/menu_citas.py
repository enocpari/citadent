"""
Módulo de menú de citas para la CLI.
Contiene las funciones de interacción con el usuario para CRUD de citas.
"""

import re
from datetime import datetime, timedelta
from backend.models.cita import Cita
from backend.models.paciente import Paciente
from backend.models.horario_atencion import formato_12h
from cli.input_helpers import input_con_cancelar, confirmar_accion, obtener_hora_12h


def agregar_cita(instancia, servicio_horarios):
    """Solicita datos y agenda una nueva cita."""
    print("\n--- Agendar Cita ---")
    
    nombre = input_con_cancelar("Ingrese el nombre del paciente")
    if nombre is None:
        print("Operación cancelada.")
        return
    
    apellido_paterno = input_con_cancelar("Ingrese el apellido paterno")
    if apellido_paterno is None:
        print("Operación cancelada.")
        return
    
    apellido_materno = input_con_cancelar("Ingrese el apellido materno")
    if apellido_materno is None:
        print("Operación cancelada.")
        return
    
    contacto = input_con_cancelar("Ingrese el numero de contacto")
    if contacto is None:
        print("Operación cancelada.")
        return
    
    while True:
        fecha_str = input_con_cancelar("Ingrese la fecha (YYYY-MM-DD)")
        if fecha_str is None:
            print("Operación cancelada.")
            return
        if re.match(r'^\d{4}-\d{2}-\d{2}$', fecha_str):
            try:
                fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
                break
            except ValueError:
                print("Error: La fecha no es valida. Verifique el dia y mes.")
        else:
            print("Error: Formato invalido. Use YYYY-MM-DD (ej: 2026-04-16)")
    
    while True:
        print("\nHora de la cita (0 para cancelar):")
        hora = obtener_hora_12h()
        if hora is None:
            print("Operación cancelada.")
            return
        
        if not servicio_horarios.hay_horarios_configurados():
            print("Error: No hay horarios de atencion configurados. Por favor, contacte al administrador.")
            continue
        
        valido, mensaje = servicio_horarios.verificar_horario_atencion(fecha, hora)
        if not valido:
            print(f"Error: {mensaje}")
            continue
        
        if not instancia.verificar_disponibilidad(fecha, hora):
            hora_12 = formato_12h(hora)
            print(f"Error: Ya existe una cita el {fecha} a las {hora_12}")
            print("Por favor, ingrese otro horario.")
            continue
        
        break
    
    hora_12 = formato_12h(hora)
    print("\n--- Resumen de la Cita ---")
    print(f"  Paciente: {nombre} {apellido_paterno} {apellido_materno}")
    print(f"  Contacto: {contacto}")
    print(f"  Fecha: {fecha}")
    print(f"  Hora: {hora_12}")
    
    if not confirmar_accion("¿Confirmar agendar cita?"):
        print("Operación cancelada.")
        return
    
    id = len(instancia.citas) + 1
    nueva_cita = Cita(id, nombre, apellido_paterno, apellido_materno, contacto, fecha, hora)
    instancia.agregar_cita(nueva_cita)
    print("Cita agendada correctamente")


def mostrar_citas(instancia):
    """Muestra todas las citas."""
    instancia.mostrar_citas()


def buscar_cita_interactivo(instancia):
    """Busca cita por ID."""
    id = int(input("Ingrese el ID de la cita: "))
    cita = instancia.buscar_cita(id)
    if cita:
        print(f" Cita encontrada: {cita}")
    else:
        print("No se encontro una cita con ese ID")


def citas_hoy(instancia):
    """Muestra citas del día."""
    citas = instancia.citas_hoy()
    if citas:
        print(f"Citas para hoy ({datetime.now().date()}):")
        for c in citas:
            print(f"  {c}")
    else:
        print("No hay citas para hoy")


def citas_manana(instancia):
    """Muestra citas de mañana."""
    manana = datetime.now().date() + timedelta(days=1)
    citas = instancia.citas_manana()
    if citas:
        print(f"Citas para manana ({manana}):")
        for c in citas:
            print(f"  {c}")
    else:
        print("No hay citas para manana")


def mostrar_citas_completadas(instancia):
    """Muestra las citas completadas."""
    citas = instancia.get_citas_completadas()
    if citas:
        print(f"\nCitas completadas ({len(citas)}):")
        for c in citas:
            print(f"  {c}")
    else:
        print("No hay citas completadas.")


def mostrar_citas_canceladas(instancia):
    """Muestra las citas canceladas."""
    citas = instancia.get_citas_canceladas()
    if citas:
        print(f"\nCitas canceladas ({len(citas)}):")
        for c in citas:
            print(f"  {c}")
def buscar_por_fecha_interactivo(instancia):
    """Busca citas por fecha de forma interactiva."""
    while True:
        fecha_str = input("Ingrese la fecha a buscar (YYYY-MM-DD): ")
        if re.match(r'^\d{4}-\d{2}-\d{2}$', fecha_str):
            try:
                fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
                break
            except ValueError:
                print("Error: La fecha no es valida. Verifique el dia y mes.")
        else:
            print("Error: Formato invalido. Use YYYY-MM-DD (ej: 2026-04-16)")
    
    citas = instancia.buscar_por_fecha(fecha)
    if citas:
        print(f"\nSe encontraron {len(citas)} cita(s) para el {fecha}:")
        for c in citas:
            print(f"  {c}")
    else:
        print(f"No hay citas para el {fecha}")


def seleccionar_cita_interactiva(instancia):
    """Busca citas por criterios y permite seleccionar una."""
    print("\n--- Buscar Cita ---")
    print("Ingrese los datos de busqueda (presione Enter para omitir):")
    id_input = input("  ID de cita: ").strip()
    nombre = input("  Nombre del paciente: ").strip() or None
    apellido = input("  Apellido del paciente: ").strip() or None
    contacto = input("  Numero de contacto: ").strip() or None
    
    citas_encontradas = []
    
    if id_input:
        try:
            id_int = int(id_input)
            cita = instancia.buscar_cita(id_int)
            if cita:
                return (cita, id_int)
            else:
                print("No se encontro una cita con ese ID.")
                return (None, None)
        except ValueError:
            print("ID invalido. Buscando por otros criterios...")
    
    if nombre or apellido or contacto:
        citas_encontradas = instancia.buscar_por_paciente(nombre, apellido, contacto)
    
    if not citas_encontradas:
        print("No se encontraron citas con esos criterios.")
        return (None, None)
    
    if len(citas_encontradas) == 1:
        cita = citas_encontradas[0]
        print(f"\nSe encontro 1 cita:")
        print(f"  {cita}")
        confirmacion = input("Es esta la cita que desea seleccionar? (s/n): ").strip().lower()
        if confirmacion == 's':
            return (cita, cita.id)
        else:
            return (None, None)
    
    print(f"\nSe encontraron {len(citas_encontradas)} citas:")
    for i, cita in enumerate(citas_encontradas, 1):
        print(f"  {i}. {cita}")
    
    while True:
        seleccion = input("\nSeleccione el numero de la cita (0 para cancelar): ").strip()
        if seleccion == '0':
            return (None, None)
        try:
            indice = int(seleccion) - 1
            if 0 <= indice < len(citas_encontradas):
                cita_seleccionada = citas_encontradas[indice]
                return (cita_seleccionada, cita_seleccionada.id)
            else:
                print("Numero fuera de rango. Intente de nuevo.")
        except ValueError:
            print("Entrada invalida. Ingrese un numero.")
def completar_cita(instancia, servicio_pacientes):
    """Completa una cita y registra al paciente."""
    cita, id_cita = seleccionar_cita_interactiva(instancia)
    
    if not cita:
        print("No se selecciono ninguna cita.")
        return
    
    if cita.estado != "pendiente":
        print(f"No se puede completar la cita. Estado actual: {cita.estado}")
        return
    
    if instancia.completar_cita(id_cita):
        id_paciente = len(servicio_pacientes.pacientes) + 1
        nuevo_paciente = Paciente(
            id_paciente,
            cita.nombre,
            cita.apellido_paterno,
            cita.apellido_materno,
            None,
            None,
            cita.contacto
        )
        servicio_pacientes.agregar_paciente(nuevo_paciente)
        print(f"Cita completada y paciente registrado exitosamente!")
    else:
        print("No se pudo completar la cita")


def cancelar_cita(instancia):
    """Cancela una cita."""
    cita, id_cita = seleccionar_cita_interactiva(instancia)
    
    if not cita:
        print("No se selecciono ninguna cita.")
        return
    
    if cita.estado != "pendiente":
        print(f"No se puede cancelar la cita. Estado actual: {cita.estado}")
        return
    
    if instancia.cancelar_cita(id_cita):
        print("Cita cancelada correctamente")
    else:
        print("No se pudo cancelar la cita")


def eliminar_cita(instancia):
    """Elimina una cita del registro."""
    print("\n--- Eliminar Cita ---")
    cita, id_cita = seleccionar_cita_interactiva(instancia)
    
    if not cita:
        print("No se seleccionó ninguna cita.")
        return
    
    print(f"\n--- Datos de la Cita ---")
    print(f"  Paciente: {cita.nombre} {cita.apellido_paterno} {cita.apellido_materno}")
    print(f"  Contacto: {cita.contacto}")
    print(f"  Fecha: {cita.fecha}")
    print(f"  Hora: {formato_12h(cita.hora)}")
    print(f"  Estado: {cita.estado}")
    
    if not confirmar_accion("¿Está seguro de eliminar esta cita?"):
        print("Operación cancelada.")
        return
    
    if instancia.eliminar_cita(id_cita):
        print("Cita eliminada correctamente")
    else:
        print("No se pudo eliminar la cita")


def buscar_por_paciente_interactivo(instancia):
    """Busca citas por datos del paciente."""
    print("\n--- Buscar Cita por Paciente ---")
    print("Ingrese los datos de busqueda (presione Enter para omitir):")
    nombre = input("  Nombre: ").strip() or None
    apellido = input("  Apellido: ").strip() or None
    contacto = input("  Numero de contacto: ").strip() or None
    
    citas = instancia.buscar_por_paciente(nombre, apellido, contacto)
    
    if citas:
        print(f"\nSe encontraron {len(citas)} cita(s):")
        for c in citas:
            print(f"  {c}")
    else:
        print("No se encontraron citas con esos criterios")
def menu_buscar_citas(instancia):
    """Submenú de búsqueda de citas."""
    while True:
        print("\n=== Buscar Cita ===")
        print("1. Buscar por ID")
        print("2. Buscar por paciente/contacto")
        print("3. Buscar por fecha")
        print("4. Volver al menu citas")
        opcion = input("Seleccione opcion: ")
        match opcion:
            case "1":
                buscar_cita_interactivo(instancia)
            case "2":
                buscar_por_paciente_interactivo(instancia)
            case "3":
                buscar_por_fecha_interactivo(instancia)
            case "4":
                break
            case _:
                print("Opcion no valida")


def menu_gestionar_citas(instancia, servicio_pacientes):
    """Submenú de gestión de citas (completar, cancelar, eliminar)."""
    while True:
        print("\n=== Gestionar Citas ===")
        print("1. Ver citas completadas")
        print("2. Ver citas canceladas")
        print("3. Completar cita")
        print("4. Cancelar cita")
        print("5. Eliminar cita")
        print("6. Volver al menu citas")
        opcion = input("Seleccione opcion: ")
        match opcion:
            case "1":
                mostrar_citas_completadas(instancia)
            case "2":
                mostrar_citas_canceladas(instancia)
            case "3":
                completar_cita(instancia, servicio_pacientes)
            case "4":
                cancelar_cita(instancia)
            case "5":
                eliminar_cita(instancia)
            case "6":
                break
            case _:
                print("Opcion no valida")


def menu_citas(instancia, servicio_horarios, servicio_pacientes):
    """Menú principal de citas."""
    while True:
        print("\n=== Menu Citas ===")
        print("1. Agendar nueva cita")
        print("2. Mostrar todas las citas")
        print("3. Buscar cita")
        print("4. Citas de hoy")
        print("5. Citas de manana")
        print("6. Gestionar Citas")
        print("7. Volver al menu principal")
        opcion = input("Seleccione opcion: ")
        match opcion:
            case "1":
                agregar_cita(instancia, servicio_horarios)
            case "2":
                mostrar_citas(instancia)
            case "3":
                menu_buscar_citas(instancia)
            case "4":
                citas_hoy(instancia)
            case "5":
                citas_manana(instancia)
            case "6":
                menu_gestionar_citas(instancia, servicio_pacientes)
            case "7":
                break
            case _:
                print("Opcion no valida")
    else:
        print("No hay citas canceladas.")