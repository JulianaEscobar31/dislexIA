from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
import numpy as np
import joblib

class DislexiaModel:
    def __init__(self):
        self.rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.svm_model = SVC(kernel='rbf', probability=True, random_state=42)
        self.scaler = StandardScaler()
        
    def procesar_datos_lectura(self, tiempo_lectura, errores, pausas, repeticiones):
        features = np.array([[
            tiempo_lectura,
            errores,
            pausas,
            repeticiones,
            errores / max(tiempo_lectura, 1),  # Tasa de errores por segundo
            pausas / max(tiempo_lectura, 1),   # Tasa de pausas por segundo
            repeticiones / max(tiempo_lectura, 1)  # Tasa de repeticiones por segundo
        ]])
        return self.scaler.transform(features)
    
    def procesar_datos_dictado(self, tiempo_escritura, errores_ortograficos, correcciones, texto_original, texto_escrito):
        # Calcular métricas adicionales para dictado
        palabras_original = len(texto_original.split())
        palabras_escritas = len(texto_escrito.split())
        palabras_correctas = sum(1 for a, b in zip(texto_original.split(), texto_escrito.split()) if a == b)
        
        features = np.array([[
            tiempo_escritura,
            errores_ortograficos,
            correcciones,
            palabras_correctas / max(palabras_original, 1),  # Precisión de palabras
            errores_ortograficos / max(palabras_escritas, 1),  # Tasa de errores por palabra
            correcciones / max(tiempo_escritura, 1),  # Tasa de correcciones por segundo
            abs(palabras_original - palabras_escritas) / max(palabras_original, 1)  # Diferencia en longitud
        ]])
        return self.scaler.transform(features)
    
    def predecir_dislexia(self, features_procesados, tipo_ejercicio='lectura'):
        rf_prob = self.rf_model.predict_proba(features_procesados)[0]
        svm_prob = self.svm_model.predict_proba(features_procesados)[0]
        
        # Ponderar las predicciones según el tipo de ejercicio
        if tipo_ejercicio == 'lectura':
            peso_rf = 0.6  # Mayor peso para lectura
            peso_svm = 0.4
        else:  # dictado
            peso_rf = 0.4
            peso_svm = 0.6  # Mayor peso para dictado
            
        probabilidad_combinada = (rf_prob * peso_rf + svm_prob * peso_svm) / (peso_rf + peso_svm)
        
        return {
            'probabilidad_dislexia': float(probabilidad_combinada[1]),
            'nivel_confianza': float(max(rf_prob[1], svm_prob[1])),
            'tipo_ejercicio': tipo_ejercicio
        }
    
    def guardar_modelo(self, ruta):
        modelo_data = {
            'rf_model': self.rf_model,
            'svm_model': self.svm_model,
            'scaler': self.scaler
        }
        joblib.dump(modelo_data, ruta)
    
    def cargar_modelo(self, ruta):
        modelo_data = joblib.load(ruta)
        self.rf_model = modelo_data['rf_model']
        self.svm_model = modelo_data['svm_model']
        self.scaler = modelo_data['scaler'] 