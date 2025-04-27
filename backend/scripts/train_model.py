import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# Datos de ejemplo para entrenamiento inicial
X_train = np.array([
    [10, 2, 1, 0.8],  # [tiempo_respuesta, errores_ortograficos, repeticiones, comprension_lectora]
    [15, 5, 3, 0.6],
    [8, 1, 0, 0.9],
    [20, 7, 4, 0.5],
    [12, 3, 2, 0.7],
    [25, 8, 5, 0.4],
    [9, 1, 1, 0.85],
    [18, 6, 3, 0.55],
    [13, 4, 2, 0.75],
    [22, 7, 4, 0.45]
])

# Etiquetas (0: no dislexia, 1: posible dislexia)
y_train = np.array([0, 1, 0, 1, 0, 1, 0, 1, 0, 1])

# Crear y entrenar el modelo
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=None,
    min_samples_split=2,
    min_samples_leaf=1,
    random_state=42
)

# Entrenar el modelo
model.fit(X_train, y_train)

# Guardar el modelo
model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app', 'model_dislexia.pkl')
joblib.dump(model, model_path)

print(f"Modelo entrenado y guardado en {model_path}")
