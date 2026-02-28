from flask import Blueprint, request, jsonify
from app.models.tarea_modelo import TareaModelo
from app.config.bd import obtener_conexion

tareas_bp = Blueprint("tareas", __name__)


# ✅ Obtener tareas (hice que el usuario_id sea opcional o use GET simple)
@tareas_bp.route("/tareas/<int:usuario_id>", methods=["GET"])
def obtener_tareas(usuario_id):

    tareas = TareaModelo.obtener_tareas_por_usuario(usuario_id)
    return jsonify(tareas)

# ✅ Crear tarea (Mantenlo como POST, pero pruébalo con Postman, no con el navegador)
@tareas_bp.route("/tareas", methods=["POST"])
def crear_tarea():
    datos = request.json

    tarea_id = TareaModelo.crear_tarea(
        datos.get("usuario_id"),
        datos.get("titulo"),
        datos.get("descripcion"),
        datos.get("fecha_limite")
    )
    return jsonify({"mensaje": "Tarea creada", "id": tarea_id}), 201


# ✅ Actualizar tarea
@tareas_bp.route('/tareas/<int:id>', methods=['PUT'])
def actualizar_tarea(id):
    conn = None
    try:
        data = request.get_json()
        nuevo_estado = data.get('estado')

        # 1. Abrimos la conexión usando tu función
        conn = obtener_conexion()
        cur = conn.cursor()

        # 2. Ejecutamos el UPDATE
        cur.execute(
            "UPDATE tareas SET estado = %s WHERE id = %s",
            (nuevo_estado, id)
        )

        # 3. Guardamos los cambios
        conn.commit()
        cur.close()

        return jsonify({"mensaje": "Tarea actualizada correctamente"}), 200

    except Exception as e:
        print(f"❌ Error en el servidor: {e}")
        return jsonify({"error": str(e)}), 500
    
    finally:
        # 4. Importante: Cerramos la conexión siempre
        if conn:
            conn.close()


# ✅ Eliminar tarea
@tareas_bp.route("/tareas/<int:tarea_id>", methods=["DELETE"])
def eliminar_tarea(tarea_id):
    TareaModelo.eliminar_tarea(tarea_id)
    return jsonify({"mensaje": "Tarea eliminada"})