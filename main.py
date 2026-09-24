# ===== Servicios =====
from backend.services.dentista_services import dentista_services
from backend.services.pacientes_services import pacientes_services
from backend.services.citas_services import citas_services
from backend.services.horarios_services import horarios_services

# ===== Menus CLI =====
from cli.menu_pacientes import menu_pacientes
from cli.menu_dentistas import menu_dentistas
from cli.menu_citas import menu_citas
from cli.menu_horarios import menu_horarios_atencion

# ===== Instancias de servicios =====
servicio_pacientes = pacientes_services()
servicio_dentista = dentista_services()
servicio_citas = citas_services()
servicio_horarios = horarios_services()


def menu_admin():
    while True:
        print("\n" + "=" * 60)
        print("   SISTEMA DE GESTION - ADMINISTRADOR")
        print("=" * 60)
        print("1. Menu Pacientes")
        print("2. Menu Dentistas")
        print("3. Menu Citas")
        print("4. Menu Horarios")
        print("5. Cerrar sesion")
        opcion = input("Seleccione opcion: ")
        match opcion:
            case "1":
                menu_pacientes(servicio_pacientes)
            case "2":
                menu_dentistas(servicio_dentista)
            case "3":
                menu_citas(servicio_citas, servicio_horarios, servicio_pacientes)
            case "4":
                menu_horarios_atencion(servicio_horarios)
            case "5":
                print("Sesion cerrada.")
                break
            case _:
                print("Opcion no valida")


def main():
    while True:
        print("\n" + "=" * 60)
        print("        CITADENT - CLINICA DENTAL")
        print("=" * 60)
        print("Como desea continuar?")
        print("  1. Administrador  (gestion del sistema)")
        print("  2. Paciente       (consultas y citas)")
        print("  3. Salir")
        opcion = input("\nSeleccione opcion: ").strip()

        match opcion:
            case "1":
                clave = input("Ingrese la clave de administrador: ").strip()
                if clave == "admin123":
                    menu_admin()
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


if __name__ == "__main__":
    main()
