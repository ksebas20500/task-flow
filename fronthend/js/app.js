
const API_URL = "https://task-flow-lzav.onrender.com/api/tareas";
// 1. SEGURIDAD Y DATOS DE SESIÓN
const USUARIO_ID = localStorage.getItem('usuario_id');
const NOMBRE_USUARIO = localStorage.getItem('nombre_usuario');

// Si no hay ID de usuario, redirigir al login inmediatamente
if (!localStorage.getItem('usuario_id')) {
    window.location.href = 'login.html';
}

// Si el usuario no ha iniciado sesión, lo devolvemos al login inmediatamente
if (!USUARIO_ID) {
    window.location.href = 'login.html';
}

// 2. BIENVENIDA PERSONALIZADA
// Solo si tienes un elemento con id="nombre-bienvenida" en tu HTML
if (NOMBRE_USUARIO && document.getElementById("nombre-bienvenida")) {
    document.getElementById("nombre-bienvenida").innerText = `Hola, ${NOMBRE_USUARIO} 👋`;
}

// 3. CARGAR TAREAS (Actualizado con función de completar)
async function cargarTareas() {
    try {
        const res = await fetch(`${API_URL}/${USUARIO_ID}`);
        const tareas = await res.json();
        
        const lista = document.getElementById("lista-tareas");
        lista.innerHTML = ""; 

        tareas.forEach(tarea => {
            const li = document.createElement("li");
            // Aplicamos la clase si la tarea está completada
            li.className = tarea.estado === 'completada' ? 'completed' : '';
            
            li.innerHTML = `
                <div class="tarea-info" onclick="alternarEstado(${tarea.id}, '${tarea.estado}')" style="cursor: pointer;">
                    <strong style="${tarea.estado === 'completada' ? 'text-decoration: line-through;' : ''}">
                        ${tarea.titulo}
                    </strong>
                    <small>${tarea.fecha_limite || 'Sin fecha'}</small>
                </div>
                <div class="acciones">
                    <button class="btn-delete" onclick="eliminarTarea(${tarea.id})">🗑️</button>
                </div>
            `;
            lista.appendChild(li);
        });
    } catch (error) {
        console.error("Error al cargar tareas:", error);
    }
}

// 4. AGREGAR NUEVA TAREA (Corregido)
async function agregarTarea() {
    const titulo = document.getElementById("titulo-tarea").value.trim();
    const descripcion = document.getElementById("descripcion-tarea").value.trim();
    const fecha = document.getElementById("fecha-tarea").value;

    if (!titulo) return alert("El título es obligatorio");

    const nuevaTarea = {
        usuario_id: parseInt(USUARIO_ID),
        titulo: titulo,
        descripcion: descripcion, // Asegúrate de enviarla
        fecha_limite: fecha,
        estado: 'pendiente'
    };

    const btn = document.querySelector(".btn-add");
    btn.disabled = true;
    btn.innerText = "Guardando...";

    try {
        const respuesta = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(nuevaTarea)
        });

        if (respuesta.ok) {
            // Limpiar campos solo si tuvo éxito
            document.getElementById("titulo-tarea").value = ""; 
            document.getElementById("descripcion-tarea").value = "";
            document.getElementById("fecha-tarea").value = ""; 
            cargarTareas(); 
        } else {
            alert("Error en el servidor al guardar.");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("No se pudo conectar con el servidor.");
    } finally {
        // Esto se ejecuta SIEMPRE, haya error o no
        btn.disabled = false;
        btn.innerText = "Añadir";
    }
}

// 5. MARCAR COMO COMPLETADA / PENDIENTE (NUEVA FUNCIÓN)
async function alternarEstado(id, estadoActual) {
    const nuevoEstado = estadoActual === 'pendiente' ? 'completada' : 'pendiente';
    
    try {
        await fetch(`${API_URL}/${id}`, {
            method: "PUT", // Usamos PUT para actualizar
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ estado: nuevoEstado })
        });
        cargarTareas(); // Recargamos la lista para ver el cambio
    } catch (error) {
        console.error("Error al actualizar estado:", error);
    }
}

// 6. ELIMINAR TAREA
async function eliminarTarea(id) {
    const confirmar = confirm("¿Estás seguro de que quieres eliminar esta tarea?");
    if (confirm) {
        try {
            await fetch(`${API_URL}/${id}`, { method: "DELETE" });
            cargarTareas();
        } catch (error) {
            alert("No se pudo eliminar la tarea.");
        }
    }
}

// 7. Agregar nueva tarea (CON DESCRIPCIÓN)
async function agregarTarea() {
    const titulo = document.getElementById("titulo-tarea").value;
    const descripcion = document.getElementById("descripcion-tarea").value; // Capturamos descripción
    const fecha = document.getElementById("fecha-tarea").value;

    if (!titulo) return alert("El título es obligatorio");

    const nuevaTarea = {
        usuario_id: parseInt(USUARIO_ID),
        titulo: titulo,
        descripcion: descripcion, // La mandamos al backend
        fecha_limite: fecha
    };

    try {
        await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(nuevaTarea)
        });

        // Limpiamos los campos
        document.getElementById("titulo-tarea").value = ""; 
        document.getElementById("descripcion-tarea").value = ""; 
        document.getElementById("fecha-tarea").value = ""; 
        cargarTareas(); 
    } catch (error) {
        alert("No se pudo guardar la tarea.");
    }
}

// 8. Cargar tareas (MOSTRAR HORA Y DESCRIPCIÓN)
async function cargarTareas() {
    try {
        const res = await fetch(`${API_URL}/${USUARIO_ID}`);
        const tareas = await res.json();
        const lista = document.getElementById("lista-tareas");
        lista.innerHTML = ""; 

        tareas.forEach(tarea => {
            // Formateamos la fecha para que se vea bonita en español
            const fechaFormateada = tarea.fecha_limite 
                ? new Date(tarea.fecha_limite).toLocaleString('es-ES', { 
                    day: '2-digit', month: '2-digit', year: 'numeric', 
                    hour: '2-digit', minute: '2-digit' 
                  })
                : 'Sin fecha';

            const li = document.createElement("li");
            li.className = tarea.estado === 'completada' ? 'completed' : '';
            li.innerHTML = `
                <div class="tarea-info" onclick="alternarEstado(${tarea.id}, '${tarea.estado}')">
                    <strong>${tarea.titulo}</strong>
                    <p class="desc">${tarea.descripcion || 'Sin descripción'}</p>
                    <small>📅 ${fechaFormateada}</small>
                </div>
                <button class="btn-delete" onclick="eliminarTarea(${tarea.id})">🗑️</button>
            `;
            lista.appendChild(li);
        });
    } catch (error) {
        console.error("Error al cargar tareas:", error);
    }
}




// 9. CERRAR SESIÓN
function cerrarSesion() {
    if (confirm("¿Quieres cerrar sesión?")) {
        localStorage.clear();
        window.location.href = 'login.html';
    }
}

// Arrancar la app al cargar
document.addEventListener("DOMContentLoaded", cargarTareas);