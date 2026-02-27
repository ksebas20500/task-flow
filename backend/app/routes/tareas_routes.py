from flask import Blueprint, request, jsonify
from app.models.tarea_modelo import TareaModelo

tareas_bp = Blueprint("tareas", __name__)


# ✅ Obtener tareas (hice que el usuario_id sea opcional o use GET simple)
@tareas_bp.route("/tareas/<int:usuario_id>", methods=["GET"])
def obtener_tareas(usuario_id):
    # Esto funcionará al entrar desde el navegador a /api/tareas/1
    tareas = TareaModelo.obtener_tareas_por_usuario(usuario_id)
    return jsonify(tareas)

# ✅ Crear tarea (Mantenlo como POST, pero pruébalo con Postman, no con el navegador)
@tareas_bp.route("/tareas", methods=["POST"])
def crear_tarea():
    datos = request.json
    # Tip: Usa .get() para evitar errores si falta un campo
    tarea_id = TareaModelo.crear_tarea(
        datos.get("usuario_id"),
        datos.get("titulo"),
        datos.get("descripcion"),
        datos.get("fecha_limite")
    )
    return jsonify({"mensaje": "Tarea creada", "id": tarea_id}), 201


# ✅ Actualizar tarea
@tareas_bp.route("/tareas/<int:tarea_id>", methods=["PUT"])
def actualizar_tarea(tarea_id):
    datos = request.json

    TareaModelo.actualizar_tarea(
        tarea_id,
        datos["titulo"],
        datos.get("descripcion"),
        datos.get("fecha_limite"),
        datos.get("estado", "pending")
    )

    return jsonify({"mensaje": "Tarea actualizada"})


# ✅ Eliminar tarea
@tareas_bp.route("/tareas/<int:tarea_id>", methods=["DELETE"])
def eliminar_tarea(tarea_id):
    TareaModelo.eliminar_tarea(tarea_id)
    return jsonify({"mensaje": "Tarea eliminada"})