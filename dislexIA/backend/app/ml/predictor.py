import numpy as np
from . import model

def preparar_datos(datos_evaluacion):
    """Prepara los datos para el modelo ML"""
    return np.array([
        datos_evaluacion['tiempo_lectura'],
        datos_evaluacion['errores_escritura'],
        datos_evaluacion['comprension'],
        datos_evaluacion['errores_dictado'],
        datos_evaluacion['respuestas_gramaticales']
    ]).reshape(1, -1)

def predecir_dislexia(datos_evaluacion):
    """Realiza la predicción de dislexia"""
    try:
        X = preparar_datos(datos_evaluacion)
        prediccion = model.predict(X)
        probabilidad = model.predict_proba(X)
        
        return {
            'prediccion': int(prediccion[0]),
            'probabilidad': float(probabilidad[0][1]),  # Probabilidad de dislexia
            'confianza': 'Alta' if probabilidad[0][1] > 0.75 else 'Media' if probabilidad[0][1] > 0.5 else 'Baja'
        }
    except Exception as e:
        raise Exception(f"Error en la predicción: {str(e)}") 