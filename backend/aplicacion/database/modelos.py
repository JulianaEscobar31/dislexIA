from . import db
from datetime import datetime

class Evaluacion(db.Model):
    __tablename__ = 'evaluaciones'
    
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    tiempo_lectura = db.Column(db.Float)
    errores_escritura = db.Column(db.Integer)
    comprension = db.Column(db.Float)
    repeticiones = db.Column(db.Integer)
    prediccion = db.Column(db.Boolean)
    
    def to_dict(self):
        return {
            'id': self.id,
            'fecha': self.fecha.isoformat(),
            'tiempo_lectura': self.tiempo_lectura,
            'errores_escritura': self.errores_escritura,
            'comprension': self.comprension,
            'repeticiones': self.repeticiones,
            'prediccion': self.prediccion
        } 