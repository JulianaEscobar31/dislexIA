from fastapi import FastAPI
from .rutas import rutas

app = FastAPI()

# Registrar las rutas
app.include_router(rutas, prefix="/api")
