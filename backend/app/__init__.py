from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Inicializar extensiones
    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Importar e inicializar blueprints
    from app.routes import api
    app.register_blueprint(api, url_prefix='/api')
    
    # Crear tablas
    with app.app_context():
        db.create_all()
    
    return app
