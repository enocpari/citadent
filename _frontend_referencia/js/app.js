// ==========================================
// CONFIGURACIÓN PRINCIPAL
// ==========================================
const API_BASE = "http://127.0.0.1:8000/api";

// Estado global
let allDentists = [];
let allPatients = [];
let allAppointments = [];
let currentFilter = "all";

// 🚀 ARRANQUE: Cuando HTML cargue, iniciar todo
document.addEventListener("DOMContentLoaded", () => {
    initNavigation();
    loadDashboardData();
    initFilters();
    loadFormDependencies();
    initSearch();
});

// ==========================================
// NAVEGACIÓN LATERAL (SPA simulada)
// ==========================================
function initNavigation() {
    const navItems = document.querySelectorAll(".nav-item");
    const sections = document.querySelectorAll(".view-section");

    navItems.forEach(item => {
        item.addEventListener("click", (e) => {
            e.preventDefault();
            navItems.forEach(nav => nav.classList.remove("active"));
            sections.forEach(sec => sec.classList.remove("active"));
            item.classList.add("active");
            const targetId = item.getAttribute("data-target");
            document.getElementById(targetId).classList.add("active");

            // Cargar datos según la sección
            if (targetId === "patients") loadPatients();
            if (targetId === "doctors") loadDoctors();
            if (targetId === "appointments") loadAppointmentsTable();
        });
    });
}

// ==========================================
// BÚSQUEDA GLOBAL (por paciente en kanban)
// ==========================================
function initSearch() {
    const searchInput = document.getElementById("global-search");
    if (!searchInput) return;
    searchInput.addEventListener("input", (e) => {
        const q = e.target.value.toLowerCase();
        const filtered = allAppointments.filter(a =>
            a.patient_name.toLowerCase().includes(q) ||
            a.dentist_name.toLowerCase().includes(q) ||
            a.desc.toLowerCase().includes(q)
        );
        renderAppointments(filtered);
        updateStatistics(filtered);
    });
}

// ==========================================
// CARGA DE DEPENDENCIAS PARA FORMULARIOS
// ==========================================
async function loadFormDependencies() {
    try {
        const [resDentists, resPatients] = await Promise.all([
            fetch(`${API_BASE}/admin/dentists/`),
            fetch(`${API_BASE}/admin/patients/`)
        ]);

        allDentists = await resDentists.json();
        allPatients = await resPatients.json();

        populateDentistSelect();
    } catch (e) {
        console.error("No se pudieron cargar listas de doctores/pacientes", e);
    }
}

function populateDentistSelect() {
    const selectDentist = document.getElementById('new-appt-dentist');
    if (!selectDentist) return;
    selectDentist.innerHTML = '<option value="">Selecciona un Doctor...</option>';
    allDentists.forEach(d => {
        selectDentist.innerHTML += `<option value="${d.id}">${d.name} (${d.specialty})</option>`;
    });
}

// ==========================================
// CARGAR DASHBOARD (KANBAN)
// ==========================================
async function loadDashboardData() {
    try {
        const response = await fetch(`${API_BASE}/admin/appointments/`);
        const realAppointments = await response.json();

        allAppointments = realAppointments.map(a => ({
            id: a.id,
            patient_name: a.patient ? a.patient.name : `Paciente #${a.patient_id}`,
            dentist_name: a.dentist ? a.dentist.name : `Dr. #${a.dentist_id}`,
            start_time: a.start_time,
            status: a.status,
            desc: a.description || "Consulta General"
        }));

        applyFilterAndRender(currentFilter);

    } catch (error) {
        console.error("Error descargando datos:", error);
    }
}

function applyFilterAndRender(filter) {
    currentFilter = filter;
    const today = new Date().toISOString().split('T')[0];
    const tomorrow = new Date(Date.now() + 86400000).toISOString().split('T')[0];

    let filtered = allAppointments;
    if (filter === "today") {
        filtered = allAppointments.filter(a => a.start_time.startsWith(today));
    } else if (filter === "tomorrow") {
        filtered = allAppointments.filter(a => a.start_time.startsWith(tomorrow));
    }

    renderAppointments(filtered);
    updateStatistics(filtered);
}

// ==========================================
// PINTAR EL KANBAN
// ==========================================
function renderAppointments(appointments) {
    const listPending = document.getElementById("list-pending");
    const listCompleted = document.getElementById("list-completed");
    const listCancelled = document.getElementById("list-cancelled");

    listPending.innerHTML = "";
    listCompleted.innerHTML = "";
    listCancelled.innerHTML = "";

    let counts = { pending: 0, completed: 0, cancelled: 0 };

    appointments.forEach(appt => {
        const dateObj = new Date(appt.start_time);
        const timeStr = dateObj.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        const dateStr = dateObj.toLocaleDateString('es', { day: '2-digit', month: '2-digit', year: 'numeric' });

        let actionButtons = '';
        if (appt.status === 'pending') {
            actionButtons = `
                <div class="appt-actions-row">
                    <button class="btn-small btn-success" onclick="completeAppointment(${appt.id}, '${appt.patient_name}')" title="Marcar como Completada">
                        <i class="fa-solid fa-check"></i> Completar
                    </button>
                    <button class="btn-small btn-primary" onclick="openRescheduleModal(${appt.id}, '${appt.patient_name}', '${appt.start_time}')" title="Reprogramar">
                        <i class="fa-solid fa-clock-rotate-left"></i>
                    </button>
                    <button class="btn-small btn-secondary" onclick="cancelNormal(${appt.id}, '${appt.patient_name}')" title="Cancelar">
                        <i class="fa-solid fa-xmark"></i>
                    </button>
                    <button class="btn-emergency btn-small" onclick="cancelEmergency(${appt.id}, '${appt.patient_name}')" title="Emergencia Doctor">
                        <i class="fa-solid fa-bolt"></i> Urgencia
                    </button>
                </div>
            `;
        }

        const cardHTML = `
            <div class="appt-card ${appt.status}">
                <div class="appt-time"><i class="fa-regular fa-clock"></i> ${dateStr} — ${timeStr}</div>
                <div class="appt-patient">${appt.patient_name}</div>
                <div class="appt-desc">${appt.desc}</div>
                <div class="appt-footer" style="flex-direction: column; align-items: flex-start;">
                    <div class="appt-doctor" style="width:100%"><i class="fa-solid fa-user-doctor"></i> ${appt.dentist_name}</div>
                    ${actionButtons}
                </div>
            </div>
        `;

        if (appt.status === "pending") { listPending.innerHTML += cardHTML; counts.pending++; }
        else if (appt.status === "completed") { listCompleted.innerHTML += cardHTML; counts.completed++; }
        else if (appt.status === "cancelled") { listCancelled.innerHTML += cardHTML; counts.cancelled++; }
    });

    // Mostrar placeholders si no hay tarjetas
    if (counts.pending === 0) listPending.innerHTML = '<div class="empty-column">Sin citas pendientes</div>';
    if (counts.completed === 0) listCompleted.innerHTML = '<div class="empty-column">Sin citas completadas</div>';
    if (counts.cancelled === 0) listCancelled.innerHTML = '<div class="empty-column">Sin citas canceladas</div>';

    document.getElementById("badge-pending").innerText = counts.pending;
    document.getElementById("badge-completed").innerText = counts.completed;
    document.getElementById("badge-cancelled").innerText = counts.cancelled;
}

// ==========================================
// ACCIÓN: COMPLETAR CITA
// ==========================================
async function completeAppointment(appointmentId, patientName) {
    if (!confirm(`¿Marcar la cita de ${patientName} como COMPLETADA? Se notificará al paciente por WhatsApp.`)) return;
    try {
        const res = await fetch(`${API_BASE}/admin/appointments/${appointmentId}/complete`, { method: 'PUT' });
        if (!res.ok) {
            const err = await res.json();
            alert(`Error: ${err.detail}`);
            return;
        }
        showToast("✅ Cita completada. Paciente notificado.");
        loadDashboardData();
        loadAppointmentsTable();
    } catch (e) {
        alert("Error de conexión al completar la cita.");
    }
}

// ==========================================
// FILTROS DEL KANBAN (Todas / Hoy / Mañana)
// ==========================================
function initFilters() {
    const filters = document.querySelectorAll(".filter-btn");
    filters.forEach(btn => {
        btn.addEventListener("click", () => {
            filters.forEach(f => f.classList.remove("active"));
            btn.classList.add("active");
            applyFilterAndRender(btn.getAttribute("data-filter"));
        });
    });
}

// ==========================================
// MODALES
// ==========================================
function openNewAppointmentModal() {
    // Recargar la lista de doctores al abrir
    populateDentistSelect();
    document.getElementById('modal-overlay').classList.add('active');
    document.getElementById('modal-new-appointment').classList.add('active');
}

function openRescheduleModal(apptId, patientName, currentStartStr) {
    document.getElementById('resch-appt-id').value = apptId;
    document.getElementById('resch-patient-name').innerText = patientName;
    const dateObj = new Date(currentStartStr);
    dateObj.setMinutes(dateObj.getMinutes() - dateObj.getTimezoneOffset());
    document.getElementById('resch-appt-start').value = dateObj.toISOString().slice(0, 16);
    document.getElementById('modal-overlay').classList.add('active');
    document.getElementById('modal-reschedule').classList.add('active');
}

function closeModal(modalId) {
    document.getElementById('modal-overlay').classList.remove('active');
    document.getElementById(modalId).classList.remove('active');
}

function closeAllModals() {
    document.querySelectorAll('.modal').forEach(m => m.classList.remove('active'));
    document.getElementById('modal-overlay').classList.remove('active');
}

// ==========================================
// CREAR CITA
// ==========================================
async function submitNewAppointment(e) {
    e.preventDefault();
    const payload = {
        patient_name: document.getElementById('new-appt-patient-name').value,
        patient_phone: document.getElementById('new-appt-patient-phone').value,
        dentist_id: parseInt(document.getElementById('new-appt-dentist').value),
        start_time: new Date(document.getElementById('new-appt-start').value).toISOString(),
        end_time: new Date(document.getElementById('new-appt-end').value).toISOString(),
        description: document.getElementById('new-appt-desc').value,
        status: "pending"
    };

    try {
        const res = await fetch(`${API_BASE}/admin/appointments/`, {
            method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload)
        });
        if (!res.ok) {
            const errorData = await res.json();
            alert(`Error: ${errorData.detail}`);
            return;
        }
        showToast("✅ Cita creada y paciente notificado vía WhatsApp");
        closeModal('modal-new-appointment');
        document.getElementById('form-new-appointment').reset();
        loadDashboardData();
        loadAppointmentsTable();
    } catch (err) {
        alert("Fallo de conexión.");
    }
}

// ==========================================
// REPROGRAMAR CITA
// ==========================================
async function submitReschedule(e) {
    e.preventDefault();
    const apptId = document.getElementById('resch-appt-id').value;
    const payload = {
        start_time: new Date(document.getElementById('resch-appt-start').value).toISOString(),
        end_time: new Date(document.getElementById('resch-appt-end').value).toISOString()
    };
    try {
        const res = await fetch(`${API_BASE}/admin/appointments/${apptId}/reschedule`, {
            method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload)
        });
        if (!res.ok) {
            const err = await res.json();
            alert(`Error: ${err.detail}`);
            return;
        }
        showToast("🔄 Cita reprogramada. Paciente notificado vía WhatsApp.");
        closeModal('modal-reschedule');
        loadDashboardData();
        loadAppointmentsTable();
    } catch (err) {
        alert("Fallo de conexión.");
    }
}

// ==========================================
// CANCELAR CITA NORMAL
// ==========================================
async function cancelNormal(appointmentId, patientName) {
    if (!confirm(`¿Cancelar la cita de ${patientName}? Se notificará por WhatsApp.`)) return;
    try {
        const res = await fetch(`${API_BASE}/admin/appointments/${appointmentId}/cancel`, { method: 'PUT' });
        if (!res.ok) throw new Error("Error");
        showToast("✅ Cita cancelada. Paciente notificado.");
        loadDashboardData();
        loadAppointmentsTable();
    } catch (e) {
        alert("Error de conexión.");
    }
}

// ==========================================
// CANCELAR POR EMERGENCIA
// ==========================================
async function cancelEmergency(appointmentId, patientName) {
    if (!confirm(`⚠️ ¿Cancelar por EMERGENCIA la cita de ${patientName}? Se enviará inmediatamente un WhatsApp al paciente.`)) return;
    try {
        const res = await fetch(`${API_BASE}/admin/actions/emergency_cancel/${appointmentId}`, { method: 'POST' });
        if (res.ok) {
            showToast("🚨 Cancelación de emergencia enviada. Paciente notificado.");
            loadDashboardData();
            loadAppointmentsTable();
        } else {
            alert("Error cancelando la cita.");
        }
    } catch (e) {
        alert("El servidor backend no responde. ¿Está encendido?");
    }
}

// ==========================================
// ESTADÍSTICAS KPI
// ==========================================
function updateStatistics(appointments) {
    const today = new Date().toISOString().split('T')[0];
    const todayAppts = appointments.filter(a => a.start_time.startsWith(today)).length;
    const pending = appointments.filter(a => a.status === 'pending').length;
    const completed = appointments.filter(a => a.status === 'completed').length;
    const cancelled = appointments.filter(a => a.status === 'cancelled').length;

    animateValue("count-hoy", 0, todayAppts, 800);
    animateValue("count-pendientes", 0, pending, 800);
    animateValue("count-completadas", 0, completed, 800);
    animateValue("count-canceladas", 0, cancelled, 800);
}

function animateValue(id, start, end, duration) {
    const obj = document.getElementById(id);
    if (!obj) return;
    if (start === end) { obj.innerHTML = end; return; }
    let current = start;
    let increment = end > start ? 1 : -1;
    let range = Math.abs(end - start);
    let stepTime = Math.max(Math.floor(duration / range), 20);
    let timer = setInterval(() => {
        current += increment;
        obj.innerHTML = current;
        if (current === end) clearInterval(timer);
    }, stepTime);
}

// ==========================================
// SECCIÓN: TABLA DE CITAS COMPLETA
// ==========================================
async function loadAppointmentsTable() {
    try {
        const res = await fetch(`${API_BASE}/admin/appointments/`);
        const data = await res.json();
        const body = document.getElementById("appointments-table-body");
        if (!body) return;

        if (data.length === 0) {
            body.innerHTML = '<tr><td colspan="7" class="empty-state">No hay citas registradas.</td></tr>';
            return;
        }

        body.innerHTML = data.map(a => {
            const date = new Date(a.start_time);
            const dateStr = date.toLocaleDateString('es') + " " + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            const patientName = a.patient ? a.patient.name : `#${a.patient_id}`;
            const dentistName = a.dentist ? a.dentist.name : `#${a.dentist_id}`;
            const statusBadge = getStatusBadge(a.status);

            let actions = "";
            if (a.status === "pending") {
                actions = `
                    <button class="btn-small btn-success" onclick="completeAppointment(${a.id}, '${patientName}')" title="Completar"><i class="fa-solid fa-check"></i></button>
                    <button class="btn-small btn-primary" onclick="openRescheduleModal(${a.id}, '${patientName}', '${a.start_time}')" title="Reprogramar"><i class="fa-solid fa-clock-rotate-left"></i></button>
                    <button class="btn-small btn-secondary" onclick="cancelNormal(${a.id}, '${patientName}')" title="Cancelar"><i class="fa-solid fa-xmark"></i></button>
                `;
            }

            return `<tr>
                <td>${a.id}</td>
                <td><strong>${patientName}</strong></td>
                <td>${dentistName}</td>
                <td>${dateStr}</td>
                <td>${a.description || "Consulta General"}</td>
                <td>${statusBadge}</td>
                <td><div style="display:flex;gap:4px;">${actions}</div></td>
            </tr>`;
        }).join('');

        filterAppointmentsTable();
    } catch (e) {
        console.error("Error cargando tabla de citas:", e);
    }
}

function filterAppointmentsTable() {
    const filter = document.getElementById("appt-status-filter")?.value || "all";
    const rows = document.querySelectorAll("#appointments-table-body tr[data-status]") || [];
    // Recargar con filtro aplicado directamente al HTML
    const allRows = document.querySelectorAll("#appointments-table-body tr");
    allRows.forEach(row => {
        if (filter === "all" || !row.dataset.status) {
            row.style.display = "";
        } else {
            row.style.display = row.dataset.status === filter ? "" : "none";
        }
    });
}

// ==========================================
// SECCIÓN: TABLA DE PACIENTES
// ==========================================
async function loadPatients() {
    try {
        const res = await fetch(`${API_BASE}/admin/patients/`);
        const data = await res.json();
        const body = document.getElementById("patients-table-body");
        if (!body) return;

        if (data.length === 0) {
            body.innerHTML = '<tr><td colspan="5" class="empty-state">No hay pacientes registrados.</td></tr>';
            return;
        }

        const stateLabels = {
            0: "Ingresando nombre",
            1: "Ingresando cédula",
            2: "En menú principal",
            3: "Consulta a IA",
            4: "Eligiendo doctor",
            5: "Eligiendo fecha",
            6: "Cancelar/Reprogramar",
            7: "Nueva fecha reprog."
        };

        body.innerHTML = data.map(p => `
            <tr>
                <td>${p.id}</td>
                <td><strong>${p.name || "—"}</strong></td>
                <td><i class="fa-brands fa-whatsapp" style="color:#25D366;margin-right:5px;"></i>${p.phone_number}</td>
                <td>${p.cedula_id || "—"}</td>
                <td><span class="badge-state">${stateLabels[p.conversation_state] || `Estado ${p.conversation_state}`}</span></td>
            </tr>
        `).join('');
    } catch (e) {
        console.error("Error cargando pacientes:", e);
    }
}

// ==========================================
// SECCIÓN: CRUD DOCTORES
// ==========================================
async function loadDoctors() {
    try {
        const res = await fetch(`${API_BASE}/admin/dentists/`);
        const data = await res.json();
        allDentists = data;
        populateDentistSelect();

        const body = document.getElementById("doctors-table-body");
        if (!body) return;

        if (data.length === 0) {
            body.innerHTML = '<tr><td colspan="5" class="empty-state">No hay doctores registrados. Agrega el primero.</td></tr>';
            return;
        }

        body.innerHTML = data.map(d => `
            <tr>
                <td>${d.id}</td>
                <td><strong>${d.name}</strong></td>
                <td>${d.specialty}</td>
                <td><span class="badge-active">Activo</span></td>
                <td>
                    <div style="display:flex;gap:4px;">
                        <button class="btn-small btn-primary" onclick="openDoctorModal(${d.id}, '${d.name.replace(/'/g, "\\'")}', '${d.specialty.replace(/'/g, "\\'")}')">
                            <i class="fa-solid fa-pen"></i> Editar
                        </button>
                        <button class="btn-small btn-danger" onclick="deleteDoctor(${d.id}, '${d.name.replace(/'/g, "\\'")}')">
                            <i class="fa-solid fa-trash"></i> Eliminar
                        </button>
                    </div>
                </td>
            </tr>
        `).join('');
    } catch (e) {
        console.error("Error cargando doctores:", e);
    }
}

function openDoctorModal(id = null, name = "", specialty = "") {
    const titleEl = document.getElementById("modal-doctor-title");
    const btnEl = document.getElementById("doctor-submit-btn");
    document.getElementById("doctor-edit-id").value = id || "";
    document.getElementById("doctor-name").value = name;
    document.getElementById("doctor-specialty").value = specialty;

    if (id) {
        titleEl.innerHTML = '<i class="fa-solid fa-user-doctor" style="color:var(--accent-blue);margin-right:8px;"></i>Editar Doctor';
        btnEl.innerHTML = '<i class="fa-solid fa-floppy-disk"></i> Guardar Cambios';
    } else {
        titleEl.innerHTML = '<i class="fa-solid fa-user-doctor" style="color:var(--accent-blue);margin-right:8px;"></i>Agregar Doctor';
        btnEl.innerHTML = '<i class="fa-solid fa-floppy-disk"></i> Guardar Doctor';
    }

    document.getElementById('modal-overlay').classList.add('active');
    document.getElementById('modal-doctor').classList.add('active');
}

async function submitDoctorForm(e) {
    e.preventDefault();
    const id = document.getElementById("doctor-edit-id").value;
    const payload = {
        name: document.getElementById("doctor-name").value,
        specialty: document.getElementById("doctor-specialty").value
    };

    const isEdit = !!id;
    const url = isEdit ? `${API_BASE}/admin/dentists/${id}` : `${API_BASE}/admin/dentists/`;
    const method = isEdit ? "PUT" : "POST";

    try {
        const res = await fetch(url, {
            method, headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload)
        });
        if (!res.ok) {
            const err = await res.json();
            alert(`Error: ${err.detail}`);
            return;
        }
        showToast(isEdit ? "✅ Doctor actualizado correctamente." : "✅ Doctor agregado correctamente.");
        closeModal('modal-doctor');
        document.getElementById('form-doctor').reset();
        loadDoctors();
    } catch (err) {
        alert("Error de conexión.");
    }
}

async function deleteDoctor(id, name) {
    if (!confirm(`¿Eliminar al Dr. ${name} del sistema? Sus citas históricas se conservarán.`)) return;
    try {
        const res = await fetch(`${API_BASE}/admin/dentists/${id}`, { method: 'DELETE' });
        if (!res.ok) {
            alert("Error al eliminar el doctor.");
            return;
        }
        showToast(`🗑️ Dr. ${name} eliminado correctamente.`);
        loadDoctors();
    } catch (e) {
        alert("Error de conexión.");
    }
}

// ==========================================
// CONFIGURACIÓN
// ==========================================
function saveApiUrl() {
    const newUrl = document.getElementById("settings-api-url").value.trim();
    if (!newUrl) return;
    // En una versión más avanzada se persistiría en localStorage
    showToast("⚙️ URL guardada. Recarga el dashboard para aplicarla.");
}

// ==========================================
// HELPERS
// ==========================================
function getStatusBadge(status) {
    const map = {
        pending: '<span class="badge-status pending">Pendiente</span>',
        completed: '<span class="badge-status completed">Completada</span>',
        cancelled: '<span class="badge-status cancelled">Cancelada</span>',
        rescheduled: '<span class="badge-status rescheduled">Reprogramada</span>'
    };
    return map[status] || `<span class="badge-status">${status}</span>`;
}

function showToast(message) {
    let toast = document.getElementById("toast-notification");
    if (!toast) {
        toast = document.createElement("div");
        toast.id = "toast-notification";
        document.body.appendChild(toast);
    }
    toast.textContent = message;
    toast.classList.add("show");
    setTimeout(() => toast.classList.remove("show"), 3500);
}
