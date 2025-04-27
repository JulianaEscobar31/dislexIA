from datetime import datetime
from app import db

class Evaluacion(db.Model):
    __tablename__ = 'evaluaciones'

    id = db.Column(db.Integer, primary_key=True)
    fecha_evaluacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Métricas de ejercicios
    tiempo_respuesta = db.Column(db.Float, nullable=False)
    errores_ortograficos = db.Column(db.Integer, nullable=False)
    repeticiones = db.Column(db.Integer, nullable=False)
    comprension_lectora = db.Column(db.Float, nullable=False)
    
    # Resultados de ejercicios específicos
    ejercicio_dictado = db.Column(db.JSON, nullable=True)
    ejercicio_lectura = db.Column(db.JSON, nullable=True)
    ejercicio_comprension = db.Column(db.JSON, nullable=True)
    
    # Predicción del modelo
    prediccion = db.Column(db.Float, nullable=False)
    confianza_prediccion = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'fecha_evaluacion': self.fecha_evaluacion.isoformat(),
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