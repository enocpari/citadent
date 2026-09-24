"""
Módulo de funciones auxiliares para la interfaz CLI.
Contiene helpers para entrada de datos, confirmación y menús.
"""

import re
from datetime import time


def input_con_cancelar(prompt):
    """
    Solicita entrada al usuario con opción a cancelar.
    
    Args:
        prompt: Mensaje a mostrar al usuario.
    
    Returns:
        str o None: El valor ingresado, o None si el usuario cancela.
    """
    valor = input(f"{prompt} (0=cancelar): ").strip()
    if valor.lower() in ("0", "cancelar", "atras", "q", "quit"):
        return None
    return valor


def confirmar_accion(mensaje):
    """
    Pide confirmación S/N al usuario.
    
    Args:
        mensaje: Mensaje de confirmación a mostrar.
    
    Returns:
        bool: True si el usuario confirma, False si no.
    """
    while True:
        confirm = input(f"{mensaje} (S/N): ").strip().lower()
        if confirm in ("s", "si", "sí"):
            return True
        elif confirm in ("n", "no"):
            return False
        else:
            print("Entrada inválida. Responda S o N.")


def obtener_opcion_menu(titulo, opciones):
    """
    Muestra un menú con título y opciones, y retorna la opción seleccionada.
    
    Args:
        titulo: Título del menú.
        opciones: Dict (clave->descripción) o lista de tuplas (clave, descripción).
    
    Returns:
        str o None: La clave de la opción seleccionada, o None si cancela.
    """
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
    """
    Solicita al usuario una hora en formato 12h (H:MM AM/PM).
    
    Returns:
        time o None: Objeto time con la hora convertida a 24h, o None si cancela.
    """
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