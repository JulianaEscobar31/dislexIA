from flask import Flask
from flask_cors import CORS
from config import Config
from .database import db

def create_app():
    app = Flask(__name__)
    CORS(app)  # Habilitar CORS para el frontend
    app.config.from_object(Config)
    
    # Inicializar base de datos
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    # Registrar blueprints
    from .api.routes import api
    app.register_blueprint(api, url_prefix='/api')
    
    return app
