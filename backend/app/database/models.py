from datetime import datetime
from .. import db

class Evaluacion(db.Model):
    __tablename__ = "evaluaciones"

    id = db.Column(db.Integer, primary_key=True, index=True)
    tiempo_respuesta = db.Column(db.Float)
    errores_ortograficos = db.Column(db.Integer)
    repeticiones = db.Column(db.Integer)
    comprension_lectora = db.Column(db.Float)
    ejercicio_dictado = db.Column(db.String)
    ejercicio_lectura = db.Column(db.String)
    ejercicio_comprension = db.Column(db.String)
    prediccion = db.Column(db.Boolean)
    confianza_prediccion = db.Column(db.Float)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    id_usuario = db.Column(db.Integer)
    edad = db.Column(db.Integer)
    genero = db.Column(db.String)
    nivel_educativo = db.Column(db.String)

    def to_dict(self):
        return {
            "id": self.id,
            "tiempo_respuesta": self.tiempo_respuesta,
            "errores_ortograficos": self.errores_ortograficos,
            "repeticiones": self.repeticiones,
            "comprension_lectora": self.comprension_lectora,
            "ejercicio_dictado": self.ejercicio_dictado,
            "ejercicio_lectura": self.ejercicio_lectura,
            "ejercicio_comprension": self.ejercicio_comprension,
            "prediccion": self.prediccion,
            "confianza_prediccion": self.confianza_prediccion,
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            "id_usuario": self.id_usuario,
            "edad": self.edad,
            "genero": self.genero,
            "nivel_educativo": self.nivel_educativo
        } 