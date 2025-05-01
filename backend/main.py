from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from routes import evaluacion

app = FastAPI(
    title="DislexIA API",
    description="API para la detección de dislexia en adultos hispanohablantes",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Puerto por defecto de Vite
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear directorio temporal para archivos de audio si no existe
TEMP_DIR = os.path.join(os.path.dirname(__file__), "temp")
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

# Montar directorio de archivos estáticos
app.mount("/audio", StaticFiles(directory=TEMP_DIR), name="audio")

# Incluir rutas
app.include_router(evaluacion.router, prefix="/api/v1", tags=["evaluacion"])

@app.get("/")
async def root():
    return {
        "mensaje": "Bienvenido a la API de DislexIA",
        "version": "1.0.0",
        "estado": "activo"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True) 