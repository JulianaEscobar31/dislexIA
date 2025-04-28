from . import db
from .modelos import Evaluacion
from datetime import datetime
import pandas as pd

def guardar_evaluacion(datos_evaluacion):
    try:
        nueva_evaluacion = Evaluacion(**datos_evaluacion)
        db.session.add(nueva_evaluacion)
        db.session.commit()
        return nueva_evaluacion.id
    except Exception as e:
        db.session.rollback()
        raise e

def obtener_evaluacion(id):
    return Evaluacion.query.get_or_404(id)

def obtener_todas_evaluaciones():
    return Evaluacion.query.all()

def generar_reporte_evaluaciones(fecha_inicio=None, fecha_fin=None):
    query = Evaluacion.query
    
    if fecha_inicio:
        query = query.filter(Evaluacion.fecha >= fecha_inicio)
    if fecha_fin:
        query = query.filter(Evaluacion.fecha <= fecha_fin)
    
    evaluaciones = query.all()
    
    # Calcular estadísticas
    estadisticas = {
        'total_evaluaciones': len(evaluaciones),
        'predicciones_positivas': len([e for e in evaluaciones if e.prediccion]),
        'tiempo_lectura_promedio': sum([e.tiempo_lectura for e in evaluaciones]) / len(evaluaciones) if evaluaciones else 0,
        'errores_escritura_promedio': sum([e.errores_escritura for e in evaluaciones]) / len(evaluaciones) if evaluaciones else 0
    }
    
    return estadisticas 