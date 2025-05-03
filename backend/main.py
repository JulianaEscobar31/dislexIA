from flask import Flask, jsonify
from flask_cors import CORS
import os
from aplicacion.rutas import rutas

app = Flask(__name__)
CORS(app)

# Configuración de CORS
app.config['CORS_HEADERS'] = 'Content-Type'

# Crear directorio temporal para archivos de audio si no existe
TEMP_DIR = os.path.join(os.path.dirname(__file__), "temp")
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

# Registrar las rutas
app.register_blueprint(rutas, url_prefix='/api')

@app.route('/')
def root():
    return jsonify({
        "mensaje": "Bienvenido a la API de DislexIA",
        "version": "1.0.0",
        "estado": "activo"
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True) 