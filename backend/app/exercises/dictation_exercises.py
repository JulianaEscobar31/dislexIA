"""
Ejercicios de dictado con diferentes niveles de dificultad.
"""

DICTATION_EXERCISES = {
    "nivel_1": {
        "descripcion": "Palabras profesionales comunes",
        "palabras": [
            "administración",
            "currículum",
            "estadística",
            "supervisión",
            "coordinación",
            "estrategia",
            "innovación"
        ],
        "tiempo_maximo": 35,
        "puntaje_base": 10
    },
    "nivel_2": {
        "descripcion": "Términos técnicos y científicos",
        "palabras": [
            "biotecnología",
            "sostenibilidad",
            "paradigma",
            "correlación",
            "metodología",
            "hipótesis",
            "diagnóstico"
        ],
        "tiempo_maximo": 40,
        "puntaje_base": 15
    },
    "nivel_3": {
        "descripcion": "Palabras especializadas y complejas",
        "palabras": [
            "neurocientífico",
            "epistemológico",
            "interdisciplinario",
            "socioeconómico",
            "gubernamental",
            "antropológico",
            "psicopedagógico"
        ],
        "tiempo_maximo": 45,
        "puntaje_base": 20
    }
}

def evaluar_dictado(nivel, respuestas):
    """
    Evalúa un ejercicio de dictado.
    
    Args:
        nivel (str): Nivel del ejercicio ('nivel_1', 'nivel_2', 'nivel_3')
        respuestas (list): Lista de palabras escritas por el usuario
        
    Returns:
        dict: Resultados de la evaluación
    """
    ejercicio = DICTATION_EXERCISES[nivel]
    palabras_correctas = 0
    errores = []
    
    for palabra_correcta, respuesta in zip(ejercicio["palabras"], respuestas):
        if respuesta.lower() == palabra_correcta.lower():
            palabras_correctas += 1
        else:
            errores.append({
                "palabra": palabra_correcta,
                "escrito": respuesta,
                "tipo_error": clasificar_error(palabra_correcta, respuesta)
            })
    
    puntaje = (palabras_correctas / len(ejercicio["palabras"])) * ejercicio["puntaje_base"]
    
    return {
        "nivel": nivel,
        "palabras_correctas": palabras_correctas,
        "palabras_total": len(ejercicio["palabras"]),
        "errores": errores,
        "puntaje": puntaje
    }

def clasificar_error(palabra_correcta, respuesta):
    """
    Clasifica el tipo de error en la escritura.
    
    Args:
        palabra_correcta (str): Palabra correcta
        respuesta (str): Respuesta del usuario
        
    Returns:
        str: Tipo de error
    """
    if respuesta.lower() == palabra_correcta.lower().replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u'):
        return "acentuación"
    elif len(set(palabra_correcta.lower()) - set(respuesta.lower())) == 0:
        return "orden_letras"
    elif abs(len(palabra_correcta) - len(respuesta)) <= 2:
        return "omisión_adición"
    else:
        return "múltiple" 