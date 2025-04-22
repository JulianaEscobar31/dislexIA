from datetime import datetime
from app import db

class Evaluacion(db.Model):
    __tablename__ = 'evaluaciones'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Métricas de ejercicios
    tiempo_respuesta = db.Column(db.Float)
    errores_ortograficos = db.Column(db.Integer)
    repeticiones = db.Column(db.Integer)
    comprension_lectora = db.Column(db.Float)
    
    # Resultados de ejercicios específicos
    ejercicio_dictado = db.Column(db.JSON)
    ejercicio_lectura = db.Column(db.JSON)
    ejercicio_comprension = db.Column(db.JSON)
    
    # Predicción del modelo
    prediccion = db.Column(db.Boolean)
    confianza_prediccion = db.Column(db.Float)
    
    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'tiempo_respuesta': self.tiempo_respuesta,
            'errores_ortograficos': self.errores_ortograficos,
            'repeticiones': self.repeticiones,
            'comprension_lectora': self.comprension_lectora,
            'ejercicio_dictado': self.ejercicio_dictado,
            'ejercicio_lectura': self.ejercicio_lectura,
            'ejercicio_comprension': self.ejercicio_comprension,
            'prediccion': self.prediccion,
            'confianza_prediccion': self.confianza_prediccion
        } 