from ..modelos import ResultadoEjercicio
from ..database import db
import uuid

class ServicioEjercicios:
    @staticmethod
    def crear_id_sesion():
        return str(uuid.uuid4())

    @staticmethod
    def guardar_resultado_ejercicio(
        id_sesion: str,
        tipo_ejercicio: str,
        puntuacion: float,
        tiempo_completado: float,
        errores: int,
        metricas: dict,
        edad: int = None,
        genero: str = None
    ):
        resultado = ResultadoEjercicio(
            id_sesion=id_sesion,
            tipo_ejercicio=tipo_ejercicio,
            puntuacion=puntuacion,
            tiempo_completado=tiempo_completado,
            errores=errores,
            metricas=metricas,
            edad=edad,
            genero=genero
        )
        db.session.add(resultado)
        db.session.commit()
        return resultado

    @staticmethod
    def obtener_resultados_sesion(id_sesion: str):
        return ResultadoEjercicio.query.filter_by(id_sesion=id_sesion).all()

    @staticmethod
    def obtener_estadisticas_ejercicio(tipo_ejercicio: str = None):
        query = ResultadoEjercicio.query
        if tipo_ejercicio:
            query = query.filter_by(tipo_ejercicio=tipo_ejercicio)
        return query.all() 