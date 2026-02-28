# TaskFlow - Gestor de Tareas Minimalista 📝⚡

Repositorio académico correspondiente al desarrollo de TaskFlow, una aplicación web para la gestión de tareas por usuario mediante una arquitectura cliente–servidor con API REST en Flask.

El sistema busca facilitar la organización personal mediante la creación, consulta, actualización y eliminación de tareas asociadas a cada usuario registrado.

---

# 📌 Descripción del Proyecto

TaskFlow es un gestor de tareas minimalista inspirado en herramientas como Google Tasks y Microsoft To-Do. El sistema permite a los usuarios registrarse, iniciar sesión y administrar sus tareas personales.

La aplicación implementa:

-Arquitectura modular con Flask Blueprints

-Comunicación cliente–servidor mediante Fetch API

-Persistencia de datos en base de datos relacional

-Cifrado seguro de contraseñas

---
# 📁 Estructura del Proyecto
```plaintext
TaskFlow/
├── app/
│   ├── config/
│   │   └── bd.py
│   │
│   ├── models/
│   │   └── tarea_modelo.py
│   │
│   └── routes/
│       ├── tareas_routes.py
│       └── autentificaion_routes.py
│
├── frontend/
│   ├── css/
│   ├── js/
│   └── pages/
│
├── run.py
├── requirements.txt (opcional)
└── README.md
```
---

