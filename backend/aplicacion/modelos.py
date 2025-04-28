from .database import db
from datetime import datetime

class ResultadoEjercicio(db.Model):
    __tablename__ = "resultados_ejercicios"

    id = db.Column(db.Integer, primary_key=True, index=True)
    id_sesion = db.Column(db.String, index=True)  # Identificador único por sesión
    edad = db.Column(db.Integer, nullable=True)
    genero = db.Column(db.String, nullable=True)
    tipo_ejercicio = db.Column(db.String)  # "lectura", "dictado", "comprension"
    puntuacion = db.Column(db.Float)
    tiempo_completado = db.Column(db.Float)  # tiempo en segundos
    errores = db.Column(db.Integer)
    metricas = db.Column(db.JSON)  # métricas específicas del ejercicio
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'id_sesion': self.id_sesion,
            'edad': self.edad,
            'genero': self.genero,
            'tipo_ejercicio': self.tipo_ejercicio,
            'puntuacion': self.puntuacion,
            'tiempo_completado': self.tiempo_completado,
            'errores': self.errores,
            'metricas': self.metricas,
            'fecha_creacion': self.fecha_creacion.isoformat()
        } 