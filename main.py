# main.py

import os
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Carga las variables de un archivo .env (útil para pruebas locales)
load_dotenv()

# --- Conexión a la Base de Datos ---
# Lee la URL de conexión desde las variables de entorno del sistema.
# Render pondrá aquí la variable que configuraste.
DATABASE_URL = os.getenv("DATABASE_URL")

# Si no encuentra la variable, detiene la aplicación para evitar errores.
if not DATABASE_URL:
    raise ValueError("No se encontró la variable de entorno DATABASE_URL")

# Crea el "motor" que conecta SQLAlchemy con tu base de datos PostgreSQL.
try:
    engine = create_engine(DATABASE_URL)
except Exception as e:
    print(f"Error al crear el motor de la base de datos: {e}")
    # En un caso real, podrías manejar esto de forma más elegante.
    # Para la práctica, imprimir el error es suficiente.


# --- Creación de la Aplicación FastAPI ---
app = FastAPI(
    title="API de Lista de Tareas",
    description="Proyecto para la Práctica 3.1 de Bases de Datos - ESCOM"
)


# --- Endpoints (las URLs de tu API) ---

@app.get("/")
def read_root():
    """Endpoint principal de bienvenida."""
    return {"message": "API para la Práctica 3.1 de Bases de Datos. Accede a /tasks para ver las tareas."}


@app.get("/tasks")
def get_tasks():
    """Obtiene y devuelve todas las tareas de la base de datos."""
    try:
        with engine.connect() as connection:
            # Ejecuta una consulta SQL para seleccionar todo de la tabla 'tasks'.
            result = connection.execute(text("SELECT id, title, is_completed FROM tasks ORDER BY id;"))
            
            # Convierte los resultados en una lista de diccionarios para que sea un JSON válido.
            tasks = [{"id": row[0], "title": row[1], "is_completed": row[2]} for row in result.fetchall()]
            
            return tasks
    except Exception as e:
        # Si algo sale mal con la base de datos, devuelve un error claro.
        raise HTTPException(status_code=500, detail=f"Error al conectar con la base de datos: {e}")


# NOTA: Para cumplir con el objetivo principal (conectar y desplegar),
# este código solo implementa la lectura (GET). Para un proyecto más completo,
# añadirías más endpoints para crear (POST), actualizar (PUT) y eliminar (DELETE) tareas.