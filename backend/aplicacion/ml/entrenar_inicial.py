import numpy as np
from entrenamiento_modelo import entrenar_modelo

# Datos de entrenamiento iniciales
# Características: [tiempo_respuesta, errores_ortograficos, repeticiones, comprension_lectora]
X_train = np.array([
    # Casos sin dislexia (0)
    [15.0, 2, 1, 0.90],  # Buen rendimiento
    [17.0, 3, 2, 0.85],  # Buen rendimiento
    [20.0, 4, 2, 0.80],  # Rendimiento normal
    [22.0, 5, 3, 0.75],  # Rendimiento normal
    
    # Casos con dislexia (1)
    [35.0, 12, 6, 0.45],  # Dificultades significativas
    [40.0, 15, 7, 0.40],  # Dificultades significativas
    [32.0, 10, 5, 0.50],  # Dificultades moderadas
    [45.0, 18, 8, 0.35],  # Dificultades severas
])

# Etiquetas (0: sin dislexia, 1: con dislexia)
y_train = np.array([0, 0, 0, 0, 1, 1, 1, 1])

# Entrenar y guardar el modelo
resultado = entrenar_modelo(X_train, y_train)
print(resultado) 