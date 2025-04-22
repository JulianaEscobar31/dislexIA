import joblib
import numpy as np
from pathlib import Path

MODEL_PATH = Path(__file__).parent.parent / 'ml' / 'model_dislexia.pkl'

def load_model():
    return joblib.load(MODEL_PATH)

def preprocess_data(data):
    """
    Preprocesa los datos de entrada para el modelo.
    Orden de características:
    [tiempo_respuesta, errores_ortograficos, repeticiones, comprension_lectora, 
     palabras_dictado, errores_dictado, tiempo_lectura, errores_lectura, 
     preguntas_comprension, correctas_comprension]
    """
    features = np.array([
        data['tiempo_respuesta'],
        data['errores_ortograficos'],
        data['repeticiones'],
        data['comprension_lectora'],
        data['ejercicio_dictado']['palabras'],
        data['ejercicio_dictado']['errores'],
        data['ejercicio_lectura']['tiempo'],
        data['ejercicio_lectura']['errores'],
        data['ejercicio_comprension']['preguntas'],
        data['ejercicio_comprension']['correctas']
    ]).reshape(1, -1)
    
    return features

def predict_dislexia(data):
    """
    Realiza la predicción de dislexia basada en los datos de entrada.
    
    Args:
        data (dict): Diccionario con los datos de los ejercicios
        
    Returns:
        tuple: (prediccion, confianza)
    """
    try:
        model = load_model()
        features = preprocess_data(data)
        
        # Realizar predicción
        prediction_proba = model.predict_proba(features)[0]
        prediction = prediction_proba[1] > 0.5
        confidence = prediction_proba[1] if prediction else prediction_proba[0]
        
        return bool(prediction), float(confidence)
        
    except Exception as e:
        print(f"Error en la predicción: {str(e)}")
        return False, 0.0 