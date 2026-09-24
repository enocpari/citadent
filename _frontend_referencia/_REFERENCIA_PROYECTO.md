# 🦷 REFERENCIA DEL PROYECTO ORIGINAL: Sistema Web Clínica Dental AI

> Este archivo sirve como documentación de referencia del proyecto original. Se creó para tener un respaldo de la arquitectura, componentes y funcionalidades antes de reiniciar el proyecto desde cero.

---

## 📋 DESCRIPCIÓN GENERAL

**Nombre:** Sistema Web Clínica Dental AI  
**Propósito:** Automatizar la gestión de citas de una clínica dental mediante un bot de WhatsApp con IA, un dashboard web para administración, y recordatorios automáticos.  
**Estado:** Funcional (versión 1.0.0)

---

## 🏗️ ARQUITECTURA GENERAL

```
WhatsApp (Paciente) 
    ↕ (YCloud Webhook - API de WhatsApp)
Backend FastAPI (Python) ←→ SQLite (Base de Datos)
    ↕ (OpenAI API) 
ChatGPT (Consultas médicas virtuales)
    ↕ (APScheduler)
Recordatorios Automáticos (24h y 2h antes)
    ↕ (REST API JSON)
Dashboard Web (Frontend HTML/CSS/JS Vanilla)
```

---

## 🔧 STACK TECNOLÓGICO

| Componente | Tecnología |
|---|---|
| Backend | Python 3 + FastAPI |
| Base de Datos | SQLite + SQLAlchemy ORM |
| Frontend | HTML5, CSS3, JavaScript Vanilla |
| IA | OpenAI GPT-3.5 Turbo |
| WhatsApp | YCloud API |
| Tareas Programadas | APScheduler |
| Autenticación WhatsApp | YCloud Webhook |
| Google Calendar | Mock (no implementado realmente) |

---

## 📁 ESTRUCTURA DEL PROYECTO ORIGINAL

```
app_dental/
├── backend/
│   ├── main.py                 # Punto de entrada FastAPI
│   ├── database.py             # Conexión SQLite + SQLAlchemy
│   ├── models.py               # Modelos: Dentist, Patient, Appointment
│   ├── schemas.py              # Validadores Pydantic para la API
│   ├── requirements.txt        # Dependencias Python
│   ├── dental_clinic.db        # Base de datos SQLite
│   ├── routers/
│   │   ├── dashboard_api.py    # CRUD: pacientes, doctores, citas
│   │   ├── webhook_ycloud.py   # Bot conversacional WhatsApp (máquina de estados)
│   │   └── admin_actions.py    # Cancelación de emergencia
│   └── services/
│       ├── calendar_sync.py    # Sincronización Google Calendar (Mock)
│       ├── openai_client.py    # Cliente OpenAI GPT-3.5
│       ├── scheduler.py        # Recordatorios automáticos
│       └── ycloud_client.py    # Cliente API YCloud WhatsApp
│
├── frontend/
│   ├── index.html              # Dashboard HTML (SPA simulada)
│   ├── css/
│   │   └── styles.css          # Estilos glassmorphism
│   └── js/
│       └── app.js              # Lógica del dashboard (SPA, Kanban, CRUD)
│
├── dental_clinic.db            # Base de datos (respaldada)
├── seed_data.py                # Script para poblar datos de prueba
├── DOCUMENTACION.md            # Documentación original
└── uvicorn.log                 # Logs del servidor
```

---

## 🧠 MODELOS DE BASE DE DATOS

### Dentist (Dentistas)
| Campo | Tipo | Descripción |
|---|---|---|
| id | Integer (PK) | Identificador único |
| name | String | Nombre completo |
| specialty | String | Especialidad (Ortodoncia, Endodoncia, etc.) |
| is_active | Boolean | Si está activo en el sistema |

### Patient (Pacientes)
| Campo | Tipo | Descripción |
|---|---|---|
| id | Integer (PK) | Identificador único |
| phone_number | String (único) | Número de WhatsApp |
| name | String | Nombre completo |
| cedula_id | String (único) | Cédula de identidad |
| conversation_state | Integer | Estado del bot (0-7) |
| current_draft_appointment_id | Integer/null | ID temporal para flujo de bot |

### Appointment (Citas)
| Campo | Tipo | Descripción |
|---|---|---|
| id | Integer (PK) | Identificador único |
| patient_id | FK → Patient | Paciente atendido |
| dentist_id | FK → Dentist | Doctor que atiende |
| start_time | DateTime | Inicio de la cita |
| end_time | DateTime | Fin de la cita |
| description | Text | Motivo de la visita |
| status | String | pending / completed / cancelled / rescheduled |
| google_event_id | String/null | ID del evento en Google Calendar |
| created_at | DateTime | Fecha de creación |

---

## 🤖 MÁQUINA DE ESTADOS DEL BOT WHATSAPP

Estados del paciente (`conversation_state`):

| Estado | Descripción |
|---|---|
| 0 | **Nuevo** - Pidiendo nombre |
| 1 | **Esperando Cédula** - Registrando documento |
| 2 | **Menú Principal** - Esperando opción (1=Agendar, 2=Consultar IA, 3=Cancelar/Reprogramar) |
| 3 | **Consulta IA** - Hablando con ChatGPT sobre molestias |
| 4 | **Eligiendo Doctor** - Seleccionando especialista |
| 5 | **Eligiendo Fecha** - Escribiendo fecha y hora |
| 6 | **Gestionar Cita** - Seleccionando cita para cancelar/reprogramar |
| 7 | **Nueva Fecha** - Escribiendo nueva fecha para reprogramar |

---

## 🎯 FUNCIONALIDADES DEL DASHBOARD (FRONTEND)

- **Dashboard (Kanban):** 3 columnas (Pendientes, Completadas, Canceladas) con tarjetas de citas
- **KPIs:** Contadores animados de citas hoy, pendientes, completadas, canceladas
- **Filtros:** Todas / Hoy / Mañana
- **Búsqueda global:** Por nombre de paciente, doctor o motivo
- **CRUD Doctores:** Agregar, editar, eliminar (soft delete)
- **Tabla de Pacientes:** Lista con estado del bot conversacional
- **Tabla de Citas:** Lista completa con filtro por estado
- **Acciones en tarjetas:** Completar, Reprogramar, Cancelar, Cancelación de Emergencia
- **Modales:** Formularios para crear/reprogramar citas y editar doctores

---

## 🔌 ENDPOINTS DE LA API

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/` | Health check |
| GET | `/api/admin/appointments/` | Listar citas |
| POST | `/api/admin/appointments/` | Crear cita (con lógica anti-solapamiento) |
| PUT | `/api/admin/appointments/{id}/complete` | Marcar como completada |
| PUT | `/api/admin/appointments/{id}/cancel` | Cancelar cita |
| PUT | `/api/admin/appointments/{id}/reschedule` | Reprogramar cita |
| GET | `/api/admin/patients/` | Listar pacientes |
| GET | `/api/admin/dentists/` | Listar doctores activos |
| POST | `/api/admin/dentists/` | Crear doctor |
| PUT | `/api/admin/dentists/{id}` | Actualizar doctor |
| DELETE | `/api/admin/dentists/{id}` | Desactivar doctor (soft delete) |
| POST | `/api/webhook/ycloud` | Webhook entrante de WhatsApp |
| POST | `/api/admin/actions/emergency_cancel/{id}` | Cancelación de emergencia |

---

## ⚠️ LÓGICAS IMPORTANTES A TENER EN CUENTA

### Anti-solapamiento de citas
Antes de crear o reprogramar una cita, se verifica que el doctor no tenga otra cita activa (no cancelada) en el mismo rango horario.

### Notificaciones WhatsApp automáticas
- Al **crear** una cita → mensaje de confirmación al paciente
- Al **completar** una cita → mensaje post-consulta
- Al **cancelar** una cita → notificación de cancelación
- Al **reprogramar** → mensaje con la nueva fecha
- **Recordatorios** 24h y 2h antes (vía APScheduler)

### Cancelación de emergencia
El doctor puede cancelar citas masivamente desde el dashboard con un botón especial que envía un mensaje urgente.

---

## 🎨 DISEÑO VISUAL (FRONTEND)

- **Estilo:** Glassmorphism (cristal/translúcido)
- **Colores:** Azul (#0D8ABC) como color principal, sidebar oscuro (#1a1f36)
- **Fuente:** Inter (Google Fonts)
- **Iconos:** Font Awesome 6
- **Animaciones:** FadeIn, SlideUp, transiciones suaves
- **Responsive:** Parcialmente adaptable

---

## 🐛 BUGS CONOCIDOS EN EL FRONTEND ORIGINAL

1. **Búsqueda global rota** (`app.js` líneas 52-57): Intenta filtrar por `patient_name` y `dentist_name` como propiedades directas, pero los datos llegan como objetos anidados (`a.patient.name`).
2. **Filtro de tabla de citas no funciona** (`app.js` líneas 437-449): El HTML de las filas no incluye el atributo `data-status`, pero la función `filterAppointmentsTable()` intenta leerlo.
3. **Configuración de API URL** no se persiste en localStorage (solo muestra un toast).

---

## 🔐 SEGURIDAD

- **CORS:** Abierto a todo origen (`allow_origins=["*"]`) - Solo para desarrollo
- **API Keys:** Las claves de OpenAI y YCloud están como variables de entorno
- **Base de Datos:** Sin autenticación (sistema interno)

---

## 💡 IDEAS PARA EL NUEVO PROYECTO

- [ ] Migrar a PostgreSQL para escalabilidad
- [ ] Agregar autenticación de usuarios (login)
- [ ] Implementar Google Calendar real
- [ ] Panel de administración con roles (Admin, Doctor, Recepcionista)
- [ ] Historial clínico digital de pacientes
- [ ] Reportes y estadísticas avanzadas
- [ ] Notificaciones por Email además de WhatsApp
- [ ] App móvil (Flutter/React Native)
- [ ] Sistema de pagos integrado
- [ ] Multi-clínica (varias sucursales)

---

## 📝 CÓMO USAR ESTA REFERENCIA

1. **Frontend:** La carpeta `_frontend_referencia/` contiene el HTML, CSS y JS exactos del dashboard original. Puedes abrir `index.html` en tu navegador para ver cómo se veía.
2. **Backend:** Revisa los archivos en `backend/` para entender la lógica de la API, la máquina de estados del bot, y las integraciones.
3. **Base de datos:** El archivo `dental_clinic.db` puede consultarse con cualquier visor SQLite para ver la estructura de datos.

---

*Documento generado el 16/07/2026 - Proyecto original clonado para referencia*