const API_URL = "http://127.0.0.1:5000/api/tareas";
const USUARIO_ID = 1; // Por ahora usamos el 1 hasta terminar la Fase 5

// 1. Cargar tareas al abrir la página
async function cargarTareas() {
    const res = await fetch(`${API_URL}/${USUARIO_ID}`);
    const tareas = await res.json();
    
    const lista = document.getElementById("lista-tareas");
    lista.innerHTML = ""; // Limpiar lista

    tareas.forEach(tarea => {
        const li = document.createElement("li");
        li.className = tarea.estado === 'completada' ? 'completed' : '';
        li.innerHTML = `
            <span>${tarea.titulo} - <small>${tarea.fecha_limite || 'Sin fecha'}</small></span>
            <button onclick="eliminarTarea(${tarea.id})">🗑️</button>
        `;
        lista.appendChild(li);
    });
}

// 2. Función para agregar tarea (Lo que hacías en Postman)
async function agregarTarea() {
    const titulo = document.getElementById("titulo-tarea").value;
    const fecha = document.getElementById("fecha-tarea").value;

    const nuevaTarea = {
        usuario_id: USUARIO_ID,
        titulo: titulo,
        fecha_limite: fecha
    };

    await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(nuevaTarea)
    });

    document.getElementById("titulo-tarea").value = ""; // Limpiar input
    cargarTareas(); // Refrescar lista
}

// 3. Función para eliminar
async function eliminarTarea(id) {
    await fetch(`${API_URL}/${id}`, { method: "DELETE" });
    cargarTareas();
}

cargarTareas();