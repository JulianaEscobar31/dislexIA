import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import os

def entrenar_modelo(X_train, y_train):
    """
    Entrena un modelo de Random Forest para la detección de dislexia
    
    Args:
        X_train: Features de entrenamiento
        y_train: Labels de entrenamiento
    """
    try:
        # Crear y entrenar el modelo
        modelo = RandomForestClassifier(
            n_estimators=100,
            max_depth=None,
            min_samples_split=2,
            min_samples_leaf=1,
            random_state=42
        )
        
        # Escalar los datos
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)

        # Entrenar el modelo
        modelo.fit(X_train_scaled, y_train)

        # Guardar el modelo y el scaler
        model_path = os.path.join(os.path.dirname(__file__), 'modelo_dislexia.pkl')
        scaler_path = os.path.join(os.path.dirname(__file__), 'scaler.pkl')
        
        joblib.dump(modelo, model_path)
        joblib.dump(scaler, scaler_path)
        
        return {
            'mensaje': 'Modelo entrenado y guardado exitosamente',
            'ruta_modelo': model_path,
            'ruta_scaler': scaler_path
        }
        
    except Exception as e:
        return {
            'error': f'Error durante el entrenamiento: {str(e)}'
        } 