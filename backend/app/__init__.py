from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .database.config import SQLALCHEMY_DATABASE_URL

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # Configuración de la base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializar extensiones
    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Registrar blueprints
    from .api.routes import api
    app.register_blueprint(api, url_prefix='/api')
    
    # Importar modelos para que Alembic los detecte
    from .database.models import Evaluacion
    
    return app
