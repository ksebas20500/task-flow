from app.config.bd import obtener_conexion

class TareaModelo:

    @staticmethod
    def obtener_tareas_por_usuario(usuario_id):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        # Corregido: user_id -> usuario_id | due_date -> fecha_limite
        cursor.execute(
            "SELECT id, usuario_id, titulo, descripcion, fecha_limite, estado, created_at, updated_at "
            "FROM tareas WHERE usuario_id = %s ORDER BY fecha_limite",
            (usuario_id,)
        )

        # Convertir a lista de diccionarios para que el JSON sea legible
        columnas = [desc[0] for desc in cursor.description]
        tareas = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]

        cursor.close()
        conexion.close()
        return tareas

    @staticmethod
    def crear_tarea(usuario_id, titulo, descripcion, fecha_limite):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        # Corregido: feha_limite -> fecha_limite
        # Eliminamos created_at y updated_at del INSERT porque el DEFAULT de la BD ya los pone
        cursor.execute("""
            INSERT INTO tareas (usuario_id, titulo, descripcion, fecha_limite, estado)
            VALUES (%s, %s, %s, %s, 'pendiente')
            RETURNING id
        """, (usuario_id, titulo, descripcion, fecha_limite))

        tarea_id = cursor.fetchone()[0]

        conexion.commit()
        cursor.close()
        conexion.close()
        return tarea_id

    @staticmethod
    def actualizar_tarea(tarea_id, titulo, descripcion, fecha_limite, estado):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        # Corregido: title -> titulo | due_date -> fecha_limite | status -> estado
        cursor.execute("""
            UPDATE tareas
            SET titulo = %s,
                descripcion = %s,
                fecha_limite = %s,
                estado = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """, (titulo, descripcion, fecha_limite, estado, tarea_id))

        conexion.commit()
        cursor.close()
        conexion.close()

    @staticmethod
    def eliminar_tarea(tarea_id):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("DELETE FROM tareas WHERE id = %s", (tarea_id,))

        conexion.commit()
        cursor.close()
        conexion.close()