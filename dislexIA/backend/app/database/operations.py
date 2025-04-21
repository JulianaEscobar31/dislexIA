from . import db
from .models import Evaluacion
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
    
    # Convertir a DataFrame para análisis
    datos = []
    for eval in evaluaciones:
        datos.append(eval.to_dict())
    
    df = pd.DataFrame(datos)
    
    # Calcular estadísticas
    estadisticas = {
        'total_evaluaciones': len(evaluaciones),
        'predicciones_positivas': len([e for e in evaluaciones if e.prediccion == 1]),
        'tiempo_lectura_promedio': df['tiempo_lectura'].mean() if not df.empty else 0,
        'errores_escritura_promedio': df['errores_escritura'].mean() if not df.empty else 0
    }
    
    return estadisticas 