from flask import Flask
from flask_cors import CORS
# Asegúrate de que el nombre del archivo coincida exactamente:
from app.routes.tareas_routes import tareas_bp 
from app.routes.autentificaion_routes import auth_bp 

import os

def create_app():
    app = Flask(__name__)

    # --- SOLUCIÓN AL ERROR DE TUS CAPTURAS (CORS) ---
    # Esto permite que tu frontend en puerto 3000 se conecte al puerto 5000
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Registramos Blueprints con el prefijo /api
    # Como ya quitaste /api de auth_routes.py, esto queda perfecto
    app.register_blueprint(tareas_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api")

    return app

app = create_app()

if __name__ == '__main__':
# Usamos el puerto que asigne el servidor o el 5000 por defecto
    port = int(os.environ.get("PORT", 5000))
    # debug=False es vital para cuando subas la página a la web
    app.run(host="0.0.0.0", port=port, debug=False)