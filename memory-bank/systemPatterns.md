# Patrones del sistema — CitaDent

## Arquitectura
- **CLI principal:** `main.py` (menú raíz).
- **Capa de interfaz (CLI):** `cli/` con un archivo por entidad y helpers (`menu_pacientes.py`, `menu_dentistas.py`, `menu_citas.py`, `menu_horarios.py`, `input_helpers.py`).
- **Capa de servicios:** `backend/services/`.
- **Capa de modelos:** `backend/models/`.
- **Datos:** en memoria, por ahora.

## Patrones usados
- **Service Layer:** operaciones CRUD y búsquedas.
- **Herencia:** `Persona` -> `Dentista` / `Paciente`.
- **Métodos abstractos:** `__str__` y `tipo()` en `Persona`.
- **Flujo de datos:** input -> CLI -> servicio -> modelo -> salida.

## Relaciones
- `main.py` instancia los servicios.
- Los servicios manipulan listas de modelos.
- Los modelos encapsulan datos y representación textual.

## Rutas críticas
- Crear cita: validar disponibilidad -> guardar.
- Verificar horario: día, franja y descanso.
- Buscar/actualizar/eliminar por ID.

## Consideraciones
- Aún no hay repositorios ni ORM.
- Evitar mezclar lógica de UI con reglas de negocio.