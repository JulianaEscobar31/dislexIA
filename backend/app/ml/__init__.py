import os
import pickle

# Cargar el modelo al iniciar
model_path = os.path.join(os.path.dirname(__file__), 'model_dislexia.pkl')
with open(model_path, 'rb') as f:
    model = pickle.load(f) 