from flask import Flask
from flask_cors import CORS
from app.routes.tareas_routes import tareas_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(tareas_bp, url_prefix="/api")


@app.route("/")
def inicio():
    return {"mensaje": "API funcionando"}


if __name__ == "__main__":
    app.run(debug=True)