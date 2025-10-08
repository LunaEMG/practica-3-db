# main.py (Versión con UI y para registrar alumnos)

import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, text
from pydantic import BaseModel

# --- Modelo de Datos ---
# Esto ayuda a FastAPI a validar que los datos que llegan son correctos
class Alumno(BaseModel):
    nombre: str
    apellidos: str
    boleta: str

# --- Configuración ---
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("No se encontró la variable de entorno DATABASE_URL")

try:
    corrected_url = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://")
    engine = create_engine(corrected_url)
except Exception as e:
    print(f"Error al crear el motor de la base de datos: {e}")

app = FastAPI(title="API de Registro de Alumnos")

# --- Servir Archivos Estáticos (Frontend) ---
# Esto le dice a FastAPI que sirva cualquier archivo que esté en la carpeta 'static'
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static")


# --- Endpoints de la API ---

@app.get("/")
def read_root(request: Request):
    """Muestra la página principal (el archivo index.html)"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/alumnos")
def get_alumnos():
    """Obtiene la lista de todos los alumnos de la base de datos."""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT nombre, apellidos, boleta FROM alumnos ORDER BY id;"))
            alumnos = [{"nombre": row[0], "apellidos": row[1], "boleta": row[2]} for row in result.fetchall()]
            return alumnos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener alumnos: {e}")

@app.post("/alumnos")
def add_alumno(alumno: Alumno):
    """Añade un nuevo alumno a la base de datos."""
    try:
        with engine.connect() as connection:
            # Usamos parámetros para evitar inyección SQL
            query = text("INSERT INTO alumnos (nombre, apellidos, boleta) VALUES (:nombre, :apellidos, :boleta)")
            connection.execute(query, {"nombre": alumno.nombre, "apellidos": alumno.apellidos, "boleta": alumno.boleta})
            connection.commit() # Importante: commit para guardar los cambios
            return {"message": "Alumno añadido con éxito"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al añadir alumno: {e}")