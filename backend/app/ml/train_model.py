import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib

# Datos de entrenamiento más representativos
X = np.array([
    # Casos sin dislexia (0)
    [11.2, 2, 1, 0.88, 20, 1, 35, 1, 10, 9],  # Buen rendimiento
    [12.5, 3, 2, 0.85, 20, 2, 40, 2, 10, 8],  # Buen rendimiento
    [13.0, 3, 2, 0.80, 20, 2, 45, 2, 10, 8],  # Rendimiento normal
    [14.0, 4, 2, 0.75, 20, 3, 50, 3, 10, 7],  # Rendimiento normal
    
    # Casos con dislexia (1)
    [16.5, 9, 5, 0.42, 20, 8, 65, 7, 10, 4],  # Dificultades significativas
    [17.0, 8, 6, 0.45, 20, 7, 70, 6, 10, 4],  # Dificultades significativas
    [15.5, 7, 4, 0.50, 20, 6, 60, 5, 10, 5],  # Dificultades moderadas
    [18.0, 10, 7, 0.35, 20, 9, 75, 8, 10, 3],  # Dificultades severas
])

# Etiquetas (0: sin dislexia, 1: con dislexia)
y = np.array([0, 0, 0, 0, 1, 1, 1, 1])

# Crear y entrenar el modelo
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Guardar el modelo
joblib.dump(model, 'model_dislexia.pkl') 