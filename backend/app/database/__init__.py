from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from config import Config

db = SQLAlchemy()
migrate = Migrate()

class Evaluacion(db.Model):
    __tablename__ = 'evaluaciones'

    id = db.Column(db.Integer, primary_key=True)
    tiempo_lectura = db.Column(db.Float, nullable=True)
    errores_escritura = db.Column(db.Integer, nullable=True)
    comprension = db.Column(db.Integer, nullable=True)
    errores_dictado = db.Column(db.Integer, nullable=True)
    respuestas_gramaticales = db.Column(db.Integer, nullable=True)
    prediccion = db.Column(db.Integer, nullable=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(50), nullable=True)
    user_agent = db.Column(db.String(200), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'tiempo_lectura': self.tiempo_lectura,
            'errores_escritura': self.errores_escritura,
            'comprension': self.comprension,
            'errores_dictado': self.errores_dictado,
            'respuestas_gramaticales': self.respuestas_gramaticales,
            'prediccion': self.prediccion,
            'fecha': self.fecha.isoformat() if self.fecha else None
        }

    def __repr__(self):
        return f'<Evaluacion {self.id}>'

def init_db(app):
    db.init_app(app)
    migrate.init_app(app, db)
    
    with app.app_context():
        db.create_all() 