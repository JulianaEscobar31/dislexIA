from flask import Blueprint

# Crear el blueprint principal
rutas = Blueprint('rutas', __name__)

# Importar las rutas después de crear el blueprint
from . import rutas
