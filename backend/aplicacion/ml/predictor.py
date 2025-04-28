import numpy as np
from ..servicios.servicio_ml import ServicioML

def predecir_dislexia(datos_evaluacion):
    """
    Realiza una predicción de dislexia basada en los datos de evaluación
    """
    try:
        # Preparar características para el modelo
        features = {
            'tiempo_respuesta': datos_evaluacion.get('tiempo_lectura', 0),
            'errores_ortograficos': datos_evaluacion.get('errores_escritura', 0),
            'repeticiones': datos_evaluacion.get('repeticiones', 0),
            'comprension_lectora': datos_evaluacion.get('comprension', 0)
        }
        
        # Obtener predicción del servicio ML
        servicio_ml = ServicioML()
        resultado = servicio_ml.predict_dislexia(features)
        
        return resultado
        
    except Exception as e:
        raise Exception(f"Error en la predicción: {str(e)}") 