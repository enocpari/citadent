"""
Módulo de menú de horarios para la CLI.
Contiene las funciones de interacción con el usuario para CRUD de horarios.
"""

from backend.models.horario_atencion import HorarioAtencion, DIAS_SEMANA, formato_12h
from cli.input_helpers import input_con_cancelar, confirmar_accion, obtener_hora_12h


def agregar_horario_atencion(servicio_horarios):
    """Solicita datos y agrega un horario de atención."""
    print("\n--- Agregar Horario de Atención ---")
    
    print("\nSeleccione el dia de la semana:")
    for num, dia in DIAS_SEMANA.items():
        print(f"  {num + 1}. {dia}")
    print("  0. Cancelar")
    
    while True:
        try:
            dia_opcion = input("Dia: ").strip()
            if dia_opcion == "0":
                print("Operación cancelada.")
                return
            dia_opcion = int(dia_opcion)
            if 1 <= dia_opcion <= 7:
                dia_semana = dia_opcion - 1
                break
            else:
                print("Opción inválida. Ingrese un número del 1 al 7.")
        except ValueError:
            print("Entrada inválida. Ingrese un número.")
    
    print("\nHora de inicio de atencion (0 para cancelar):")
    hora_inicio = obtener_hora_12h()
    if hora_inicio is None:
        print("Operación cancelada.")
        return
    
    print("\nHora de fin de atencion (0 para cancelar):")
    hora_fin = obtener_hora_12h()
    if hora_fin is None:
        print("Operación cancelada.")
        return
    
    hora_inicio_descanso = None
    hora_fin_descanso = None
    agregar_descanso = input("¿Desea agregar hora de descanso? (s/n): ").strip().lower()
    
    if agregar_descanso == 's':
        print("\nHora de inicio del descanso (0 para cancelar):")
        hora_inicio_descanso = obtener_hora_12h()
        if hora_inicio_descanso is None:
            print("Operación cancelada.")
            return
        
        print("\nHora de fin del descanso (0 para cancelar):")
        hora_fin_descanso = obtener_hora_12h()
        if hora_fin_descanso is None:
            print("Operación cancelada.")
            return
    
    horario_existente = servicio_horarios.buscar_horario_por_dia(dia_semana)
    if horario_existente:
        print(f"Ya existe un horario para {DIAS_SEMANA[dia_semana]}. Se reemplazará.")
    
    print("\n--- Resumen del Horario ---")
    print(f"  Día: {DIAS_SEMANA[dia_semana]}")
    print(f"  Inicio: {formato_12h(hora_inicio)}")
    print(f"  Fin: {formato_12h(hora_fin)}")
    if hora_inicio_descanso:
        print(f"  Descanso: {formato_12h(hora_inicio_descanso)} - {formato_12h(hora_fin_descanso)}")
    
    if not confirmar_accion("¿Confirmar agregar horario?"):
        print("Operación cancelada.")
        return
    
    id_horario = len(servicio_horarios.horarios) + 1
    nuevo_horario = HorarioAtencion(
        id_horario,
        dia_semana,
        hora_inicio,
        hora_fin,
        hora_inicio_descanso,
        hora_fin_descanso,
        activo=True
    )
    servicio_horarios.agregar_horario(nuevo_horario)
    print(f"Horario agregado: {nuevo_horario}")


def mostrar_horarios_atencion(servicio_horarios):
    """Muestra todos los horarios de atención."""
    print("\n=== Horarios de Atencion ===")
    servicio_horarios.mostrar_horarios()


def eliminar_horario_atencion(servicio_horarios):
    """Elimina un horario por ID."""
    if not servicio_horarios.horarios:
        print("No hay horarios de atencion registrados.")
        return
    
    print("\n=== Eliminar Horario ===")
    print("Horarios disponibles:")
    for h in servicio_horarios.horarios:
        print(f"  {h}")
    
    while True:
        try:
            id_input = input("Ingrese el ID del horario a eliminar (0 para cancelar): ").strip()
            if id_input == '0':
                print("Operacion cancelada.")
                return
            id_horario = int(id_input)
            if servicio_horarios.eliminar_horario(id_horario):
                print("Horario eliminado correctamente.")
                return
            else:
                print("No se encontro un horario con ese ID.")
        except ValueError:
            print("Entrada invalida. Ingrese un numero.")


def menu_horarios_atencion(servicio_horarios):
    """Menú de horarios de atención."""
    while True:
        print("\n=== Horarios de Atencion ===")
        print("1. Agregar horario de atencion")
        print("2. Mostrar horarios de atencion")
        print("3. Eliminar horario")
        print("4. Volver al menu citas")
        opcion = input("Seleccione opcion: ")
        match opcion:
            case "1":
                agregar_horario_atencion(servicio_horarios)
            case "2":
                mostrar_horarios_atencion(servicio_horarios)
            case "3":
                eliminar_horario_atencion(servicio_horarios)
            case "4":
                break
            case _:
                print("Opcion no valida")