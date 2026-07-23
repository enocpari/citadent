# todos los  modulos de servicios ===========================
from backend.services.dentista_services import dentista_services
from backend.services.pacientes_services import pacientes_services
from backend.services.citas_services import citas_services
from backend.services.horarios_services import horarios_services

# todos los modulos de objetos ==============================
from backend.models.paciente import Paciente
from backend.models.dentista import Dentista
from backend.models.cita import Cita
from backend.models.horario_atencion import HorarioAtencion, DIAS_SEMANA

# modulos aparte adicionales  datetime , time ,re =====
from datetime import datetime, time
import re


# instancias  para trabajar con la clase de servicios=============
servicio_pacientes = pacientes_services()
servicio_dentista = dentista_services()
servicio_citas = citas_services()
servicio_horarios = horarios_services()


# funciones Auxiliares =========================

def input_con_cancelar(prompt):
    valor = input(f"{prompt} (0=cancelar): ").strip()
    if valor.lower() in ("0", "cancelar", "atras", "q", "quit"):
        return None
    return valor


def confirmar_accion(mensaje):
    while True:
        confirm = input(f"{mensaje} (S/N): ").strip().lower()
        if confirm in ("s", "si", "sí"):
            return True
        elif confirm in ("n", "no"):
            return False
        else:
            print("Entrada inválida. Responda S o N.")


def obtener_opcion_menu(titulo, opciones):
    print(f"\n=== {titulo} ===")
    if isinstance(opciones, dict):
        for k, v in opciones.items():
            print(f"  {k}. {v}")
        print("  0. Cancelar / Volver")
        while True:
            opc = input("Seleccione opción: ").strip()
            if opc == "0":
                return None
            if opc in opciones:
                return opc
            print("Opción inválida.")
    else:
        for k, v in opciones:
            print(f"  {k}. {v}")
        print("  0. Cancelar / Volver")
        while True:
            opc = input("Seleccione opción: ").strip()
            if opc == "0":
                return None
            for k, v in opciones:
                if opc == k:
                    return opc
            print("Opción inválida.")


def obtener_hora_12h():
    while True:
        try:
            hora_minutos = input("  Hora (H:MM) o 0 para cancelar: ").strip()
            if hora_minutos == "0":
                return None
            if re.match(r'^\d{1,2}:\d{2}$', hora_minutos):
                partes = hora_minutos.split(":")
                hora = int(partes[0])
                minutos = int(partes[1])
                if 1 <= hora <= 12 and 0 <= minutos <= 59:
                    break
                elif hora < 1 or hora > 12:
                    print("  Error: La hora debe estar entre 1 y 12.")
                else:
                    print("  Error: Los minutos deben estar entre 0 y 59.")
            else:
                print("  Error: Formato inválido. Use H:MM (ej: 3:30, 10:00)")
        except ValueError:
            print("  Error: Ingrese un formato válido (ej: 3:30, 10:00)")
    
    while True:
        periodo = input("  Periodo (AM/PM): ").strip().lower()
        if periodo == "am" or periodo == "pm":
            break
        else:
            print("  Error: Ingrese AM o PM.")
    
    es_pm = (periodo == "pm")
    if es_pm and hora != 12:
        hora_24 = hora + 12
    elif not es_pm and hora == 12:
        hora_24 = 0
    else:
        hora_24 = hora
    
    return time(hora_24, minutos)



# funciones para trabajar con la clase pacientes =====================

# AGREGAR PACIENTES
def agregar_pacientes(instancia):
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
    
# MOSTRAR PACIENTES
def mostrar_pacientes(instancia):
    instancia.mostrar_pacientes()


# BUSCAR PACIENTES
def buscar_paciente_interactivo(instancia):
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

# ELIMINAR PACIENTES
def eliminar_paciente(instancia):
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


# ACTUALIZAR PACIENTES
def actualizar_paciente(instancia):
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
      
        
# menu de pacientes ========================       
def menu_pacientes():
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
                agregar_pacientes(servicio_pacientes)
            case "2":
                mostrar_pacientes(servicio_pacientes)
            case "3":
                buscar_paciente_interactivo(servicio_pacientes)
            case "4":
                actualizar_paciente(servicio_pacientes)
            case "5":
                eliminar_paciente(servicio_pacientes)
            case "6":
                break
            case _:
                print("Opcion no valida")


# funciones para trabajar con la clase dentista =====================

# AGREGAR DENTISTA
def agregar_dentista(instancia):
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
    
# MOSTRAR DENTISTA
def mostrar_dentistas(instancia):
    instancia.mostrar_dentistas()

# BUSCAR DENTISTA
def buscar_dentista_interactivo(instancia):
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

# ACTUALIZAR DENTISTA
def actualizar_dentista(instancia):
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

# ELIMINAR DENTISTA
def eliminar_dentista(instancia):
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


# menu de dentistas ========================
def menu_dentistas():
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
                agregar_dentista(servicio_dentista)
            case "2":
                mostrar_dentistas(servicio_dentista)
            case "3":
                buscar_dentista_interactivo(servicio_dentista)
            case "4":
                actualizar_dentista(servicio_dentista)
            case "5":
                eliminar_dentista(servicio_dentista)
            case "6":
                break
            case _:
                print("Opcion no valida")


# funciones para trabajar con la clase citas =====================

# AGREGAR CITA
def agregar_cita(instancia, servicio_horarios):
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
            from backend.models.horario_atencion import formato_12h
            hora_12 = formato_12h(hora)
            print(f"Error: Ya existe una cita el {fecha} a las {hora_12}")
            print("Por favor, ingrese otro horario.")
            continue
        
        break
    
    from backend.models.horario_atencion import formato_12h
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


# MOSTRAR CITAS
def mostrar_citas(instancia):
    instancia.mostrar_citas()


# BUSCAR CITA POR ID
def buscar_cita_interactivo(instancia):
    id = int(input("Ingrese el ID de la cita: "))
    cita = instancia.buscar_cita(id)
    if cita:
        print(f" Cita encontrada: {cita}")
    else:
        print("No se encontro una cita con ese ID")


# CITAS DE HOY
def citas_hoy(instancia):
    citas = instancia.citas_hoy()
    if citas:
        print(f"Citas para hoy ({datetime.now().date()}):")
        for c in citas:
            print(f"  {c}")
    else:
        print("No hay citas para hoy")


# CITAS DE MAÑANA
def citas_manana(instancia):
    from datetime import timedelta
    manana = datetime.now().date() + timedelta(days=1)
    citas = instancia.citas_manana()
    if citas:
        print(f"Citas para manana ({manana}):")
        for c in citas:
            print(f"  {c}")
    else:
        print("No hay citas para manana")


# MOSTRAR CITAS COMPLETADAS
def mostrar_citas_completadas(instancia):
    citas = instancia.get_citas_completadas()
    if citas:
        print(f"\nCitas completadas ({len(citas)}):")
        for c in citas:
            print(f"  {c}")
    else:
        print("No hay citas completadas.")


# MOSTRAR CITAS CANCELADAS
def mostrar_citas_canceladas(instancia):
    citas = instancia.get_citas_canceladas()
    if citas:
        print(f"\nCitas canceladas ({len(citas)}):")
        for c in citas:
            print(f"  {c}")
    else:
        print("No hay citas canceladas.")


# BUSCAR CITAS POR FECHA
def buscar_por_fecha_interactivo(instancia):
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


# SELECCIONAR CITA (BUSQUEDA AVANZADA)
def seleccionar_cita_interactiva(instancia):
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


# COMPLETAR CITA
def completar_cita(instancia, servicio_pacientes):
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


# CANCELAR CITA
def cancelar_cita(instancia):
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


# ELIMINAR CITA
def eliminar_cita(instancia):
    print("\n--- Eliminar Cita ---")
    cita, id_cita = seleccionar_cita_interactiva(instancia)
    
    if not cita:
        print("No se seleccionó ninguna cita.")
        return
    
    from backend.models.horario_atencion import formato_12h
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


# BUSCAR CITA POR PACIENTE
def buscar_por_paciente_interactivo(instancia):
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


# menu de buscar citas ========================
def menu_buscar_citas():
    while True:
        print("\n=== Buscar Cita ===")
        print("1. Buscar por ID")
        print("2. Buscar por paciente/contacto")
        print("3. Buscar por fecha")
        print("4. Volver al menu citas")
        opcion = input("Seleccione opcion: ")
        match opcion:
            case "1":
                buscar_cita_interactivo(servicio_citas)
            case "2":
                buscar_por_paciente_interactivo(servicio_citas)
            case "3":
                buscar_por_fecha_interactivo(servicio_citas)
            case "4":
                break
            case _:
                print("Opcion no valida")


# menu de gestionar citas ========================
def menu_gestionar_citas():
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
                mostrar_citas_completadas(servicio_citas)
            case "2":
                mostrar_citas_canceladas(servicio_citas)
            case "3":
                completar_cita(servicio_citas, servicio_pacientes)
            case "4":
                cancelar_cita(servicio_citas)
            case "5":
                eliminar_cita(servicio_citas)
            case "6":
                break
            case _:
                print("Opcion no valida")


# menu de citas ========================
def menu_citas():
    while True:
        print("\n=== Menu Citas ===")
        print("1. Agendar nueva cita")
        print("2. Mostrar todas las citas")
        print("3. Buscar cita")
        print("4. Citas de hoy")
        print("5. Citas de manana")
        print("6. Horarios de atencion")
        print("7. Gestionar Citas")
        print("8. Volver al menu principal")
        opcion = input("Seleccione opcion: ")
        match opcion:
            case "1":
                agregar_cita(servicio_citas, servicio_horarios)
            case "2":
                mostrar_citas(servicio_citas)
            case "3":
                menu_buscar_citas()
            case "4":
                citas_hoy(servicio_citas)
            case "5":
                citas_manana(servicio_citas)
            case "6":
                menu_horarios_atencion()
            case "7":
                menu_gestionar_citas()
            case "8":
                break
            case _:
                print("Opcion no valida")


# funciones para trabajar con la clase horarios =====================

# AGREGAR HORARIO DE ATENCION
def agregar_horario_atencion():
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
    
    from backend.models.horario_atencion import formato_12h
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


# MOSTRAR HORARIOS DE ATENCION
def mostrar_horarios_atencion():
    print("\n=== Horarios de Atencion ===")
    servicio_horarios.mostrar_horarios()


# ELIMINAR HORARIO DE ATENCION
def eliminar_horario_atencion():
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
            
# menu de horarios ========================
def menu_horarios_atencion():
    while True:
        print("\n=== Horarios de Atencion ===")
        print("1. Agregar horario de atencion")
        print("2. Mostrar horarios de atencion")
        print("3. Eliminar horario")
        print("4. Volver al menu citas")
        opcion = input("Seleccione opcion: ")
        match opcion:
            case "1":
                agregar_horario_atencion()
            case "2":
                mostrar_horarios_atencion()
            case "3":
                eliminar_horario_atencion()
            case "4":
                break
            case _:
                print("Opcion no valida")


# menu principal del sistema ========================
def main():
    while True:
        print("\n" + "="*60)
        print("        CITADENT - CLINICA DENTAL")
        print("="*60)
        print("Como desea continuar?")
        print("  1. Administrador  (gestion del sistema)")
        print("  2. Paciente       (consultas y citas)")
        print("  3. Salir")
        opcion = input("\nSeleccione opcion: ").strip()
 
        match opcion:
            case "1":
                clave = input("Ingrese la clave de administrador: ").strip()
                if clave == "admin123":
                    menu_principal()
                else:
                    print("Clave incorrecta.")
            case "2":
                print("\nBienvenido al sistema de citas de CitaDent!")
                print("Aqui podras consultar tus citas, horarios disponibles y mas.")
                print("Por ahora esta funcionalidad esta en desarrollo. Por favor, contacte a la clinica para agendar o consultar citas.")
            case "3":
                print("Hasta pronto!")
                break
            case _:
                print("Opcion no valida.")
                
# menu de administrador ========================
def menu_principal():
    while True:
        print("\n" + "="*60)
        print("   SISTEMA DE GESTION - ADMINISTRADOR")
        print("="*60)
        print("1. Menu Pacientes")
        print("2. Menu Dentistas")
        print("3. Menu Citas")
        print("4. Cerrar sesion")
        opcion = input("Seleccione opcion: ")
        match opcion:
            case "1":
                menu_pacientes()
            case "2":
                menu_dentistas()
            case "3":
                menu_citas()
            case "4":
                print("Sesion cerrada.")
                break
            case _:
                print("Opcion no valida")
 
if __name__ == "__main__":
    main()