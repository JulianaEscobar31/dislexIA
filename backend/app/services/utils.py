from functools import wraps
from flask import jsonify

def validar_datos_evaluacion(data):
    """Valida los datos de una evaluación"""
    errores = []
    campos_requeridos = [
        'tiempo_respuesta',
        'errores_ortograficos',
        'repeticiones',
        'comprension_lectora',
        'ejercicio_dictado',
        'ejercicio_lectura',
        'ejercicio_comprension',
        'prediccion',
        'confianza_prediccion'
    ]
    
    for campo in campos_requeridos:
        if campo not in data:
            errores.append(f"Falta el campo requerido: {campo}")
            
    # Validaciones específicas
    if 'tiempo_respuesta' in data and not isinstance(data['tiempo_respuesta'], (int, float)):
        errores.append("tiempo_respuesta debe ser un número")
        
    if 'errores_ortograficos' in data and not isinstance(data['errores_ortograficos'], int):
        errores.append("errores_ortograficos debe ser un número entero")
        
    if 'prediccion' in data and not isinstance(data['prediccion'], bool):
        errores.append("prediccion debe ser un valor booleano")
        
    if 'confianza_prediccion' in data:
        confianza = data['confianza_prediccion']
        if not isinstance(confianza, (int, float)) or confianza < 0 or confianza > 1:
            errores.append("confianza_prediccion debe ser un número entre 0 y 1")
            
    return errores

def manejar_errores(f):
    """Decorador para manejar errores en las rutas"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({
                'error': str(e),
                'tipo': type(e).__name__
            }), 500
    return decorated_function 