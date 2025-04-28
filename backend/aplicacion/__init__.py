from flask import Flask
from flask_cors import CORS
from config import Config
from .database import db, init_db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    CORS(app)
    init_db(app)
    
    from .rutas import rutas as main_rutas
    app.register_blueprint(main_rutas)
    
    return app
