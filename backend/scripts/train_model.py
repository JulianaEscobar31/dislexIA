import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle

# Datos simulados
data = pd.DataFrame({
    'tiempo_lectura': [12, 18, 10, 20, 15, 22, 8, 25, 17, 14],
    'errores_escritura': [1, 5, 0, 6, 3, 7, 0, 6, 4, 2],
    'es_dislexico': [0, 1, 0, 1, 0, 1, 0, 1, 1, 0]  # 1 = disléxico
})

# Separar X y y
X = data[['tiempo_lectura', 'errores_escritura']]
y = data['es_dislexico']

# Entrenar modelo
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Guardar modelo entrenado
with open("app/model_dislexia.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Modelo entrenado y guardado en app/model_dislexia.pkl")
