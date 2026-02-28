from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.config.bd import obtener_conexion

# Creamos el Blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    nombre = data.get('nombre')
    email = data.get('email')
    password = data.get('password')
    
    # Ciframos la contraseña antes de guardarla
    hash_pw = generate_password_hash(password)
    
    conn = obtener_conexion()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO usuarios (nombre, email, password_hash) VALUES (%s, %s, %s) RETURNING id",
            (nombre, email, hash_pw)
        )
        usuario_id = cur.fetchone()[0]
        conn.commit()
        return jsonify({"mensaje": "Usuario creado con éxito", "usuario_id": usuario_id}), 201
    except Exception as e:
        return jsonify({"error": "El email ya está registrado"}), 400
    finally:
        cur.close()
        conn.close()

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    conn = obtener_conexion()
    cur = conn.cursor()
    cur.execute("SELECT id, password_hash, nombre FROM usuarios WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    
    # Verificamos si el usuario existe y si la contraseña coincide con el hash
    if user and check_password_hash(user[1], password):
        return jsonify({
            "mensaje": "Login exitoso",
            "usuario_id": user[0],
            "nombre": user[2]
        }), 200
    
    return jsonify({"error": "Correo o contraseña incorrectos"}), 401