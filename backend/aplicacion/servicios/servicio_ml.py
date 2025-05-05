import joblib
import numpy as np
from sklearn.preprocessing import StandardScaler
import os

class ServicioML:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.load_model()
        
    def load_model(self):
        """Carga el modelo entrenado y el scaler"""
        model_path = os.path.join(os.path.dirname(__file__), '..', 'ml', 'modelo_dislexia.pkl')
        scaler_path = os.path.join(os.path.dirname(__file__), '..', 'ml', 'scaler.pkl')
        if os.path.exists(model_path):
            self.model = joblib.load(model_path)
        else:
            raise FileNotFoundError("Modelo no encontrado")
        if os.path.exists(scaler_path):
            self.scaler = joblib.load(scaler_path)
        else:
            print("Advertencia: scaler.pkl no encontrado, se usará StandardScaler() sin entrenar. Esto puede causar errores si no se entrena primero.")
            
    def predict_dislexia(self, features):
        """Realiza una predicción usando el modelo entrenado"""
        if not self.model:
            raise Exception("Modelo no cargado")
            
        # Preparar features
        feature_names = [
            'tiempo_respuesta',
            'errores_ortograficos',
            'repeticiones',
            'comprension_lectora'
        ]
        
        X = np.array([[
            features.get('tiempo_respuesta', 0),
            features.get('errores_ortograficos', 0),
            features.get('repeticiones', 0),
            features.get('comprension_lectora', 0)
        ]])
        
        # Escalar datos
        X_scaled = self.scaler.transform(X)
        
        # Realizar predicción
        try:
            probabilidad = self.model.predict_proba(X_scaled)[0]
            prediccion = self.model.predict(X_scaled)[0]
            probabilidad_dislexia = float(probabilidad[1])  # Probabilidad de la clase 'dislexia'
            return {
                'prediccion': bool(prediccion),
                'probabilidad': probabilidad_dislexia,
                'features_utilizados': {
                    name: float(value) for name, value in zip(feature_names, X[0])
                }
            }
        except Exception as e:
            return {
                'error': f"Error en la predicción: {str(e)}",
                'prediccion': False,
                'probabilidad': 0.0
            }
            
    def entrenar_modelo(self, X_train, y_train):
        """Entrena o actualiza el modelo con nuevos datos"""
        # Escalar datos
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        # Entrenar modelo
        self.model.fit(X_train_scaled, y_train)
        
        # Guardar modelo
        model_path = os.path.join(os.path.dirname(__file__), '..', 'ml', 'modelo_dislexia.pkl')
        joblib.dump(self.model, model_path)
        
        return {
            'mensaje': 'Modelo entrenado y guardado exitosamente',
            'ruta_modelo': model_path
        }

    def evaluar_ejercicio(self, tipo, datos):
        """
        Evalúa los datos del ejercicio usando el modelo de ML
        """
        # Por ahora retornamos una predicción simulada
        # TODO: Implementar el modelo real de ML
        return {
            'prediccion': 0.85,  # Probabilidad de dislexia
            'confianza': 0.89    # Confianza en la predicción
        }

servicio_ml = ServicioML() 