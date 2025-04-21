from flask import jsonify
from functools import wraps

def validar_datos_evaluacion(data):
    campos_requeridos = {
        'tiempo_lectura': float,
        'errores_escritura': int,
        'comprension': int,
        'errores_dictado': int,
        'respuestas_gramaticales': int,
        'prediccion': int
    }
    
    errores = []
    
    for campo, tipo in campos_requeridos.items():
        if campo not in data:
            errores.append(f'El campo {campo} es requerido')
        else:
            try:
                data[campo] = tipo(data[campo])
            except (ValueError, TypeError):
                errores.append(f'El campo {campo} debe ser de tipo {tipo.__name__}')
    
    return errores

def manejar_errores(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return wrapper
