# Contexto activo — CitaDent

## Foco actual
- Documentar la arquitectura y el estado del proyecto.
- Mantener la separación entre modelos y servicios.
- Seguir evolucionando la CLI.

## Cambios recientes
- Se movió la gestión de horarios al menú de administrador.
- Se renombró `menu_principal` a `menu_admin`.
- Se reorganizó `main.py`.
- Se añadieron modelos y servicios base.
- Se separó la capa CLI en módulos independientes (`cli/`): `menu_pacientes.py`, `menu_dentistas.py`, `menu_citas.py`, `menu_horarios.py` y `input_helpers.py`.
- `main.py` quedó reducido a solo el menú raíz y la importación de los submódulos CLI.

## Próximos pasos
- Persistencia en base de datos.
- Mejorar validaciones.
- Añadir tests.
- Evaluar frontend web.
- Integrar IA y WhatsApp más adelante.

## Decisiones activas
- Mantener Python y CLI por ahora.
- Usar listas en memoria hasta migrar a DB.
- Mantener nombres y mensajes en español.