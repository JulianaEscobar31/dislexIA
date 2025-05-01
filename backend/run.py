from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from aplicacion.rutas import rutas

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar las rutas
app.include_router(rutas, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("run:app", host="0.0.0.0", port=5000, reload=True)
