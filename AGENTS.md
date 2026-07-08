# AGENTS.md - CitaDent

## Running the App

```bash
python3 main.py
```

## Authentication

- Admin password: `admin123` (hardcoded in `main.py:963`)
- Accessible via menu option 1 at startup

## Architecture

- **Entry point**: `main.py` (CLI menu system)
- **Models**: `backend/models/` - Paciente, Dentista, Cita, HorarioAtencion (inherit from Persona abstract class)
- **Services**: `backend/services/` - CRUD business logic
- **Data storage**: In-memory (no database)
- **No external dependencies**: Pure Python stdlib

## Menu Hierarchy

1. `main()` → login choice
2. Option 1 (Admin) → `menu_principal()` → Patients / Dentists / Citas / Horarios
3. Option 2 (Patient) → Stub (not implemented)

## Key Conventions

- All IDs are auto-incremented integers
- Citas have states: pendiente, completada, cancelada
- Horarios include descanso periods per weekday
- Time input uses 12h format with AM/PM (converted internally to 24h)

## Development Notes

- The frontend directory (`fronted/`) is empty
- Chatbot service exists but not integrated in current flow (per documentary.md)
- No tests, no linter, no typecheck configured