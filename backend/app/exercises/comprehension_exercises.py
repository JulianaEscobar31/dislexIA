"""
Ejercicios de comprensión con diferentes niveles de dificultad.
"""

COMPREHENSION_EXERCISES = {
    "nivel_1": {
        "titulo": "Análisis del Impacto de la IA",
        "texto_referencia": "texto_ia_mercado_laboral",
        "preguntas": [
            {
                "tipo": "análisis",
                "pregunta": "¿Qué implicaciones tiene la automatización para el desarrollo profesional según el texto?",
                "opciones": [
                    "La necesidad de adaptación continua y aprendizaje permanente",
                    "La eliminación completa de trabajos humanos",
                    "La reducción de la importancia de la formación profesional"
                ],
                "correcta": 0,
                "explicacion": "El texto enfatiza la adaptabilidad y el aprendizaje continuo como competencias esenciales.",
                "puntaje": 5
            },
            {
                "tipo": "inferencia",
                "pregunta": "¿Qué se puede inferir sobre el futuro del mercado laboral?",
                "opciones": [
                    "Será exclusivamente tecnológico",
                    "Requerirá una combinación de habilidades técnicas y adaptativas",
                    "Mantendrá las mismas competencias actuales"
                ],
                "correcta": 1,
                "explicacion": "El texto sugiere una transformación que combina tecnología con nuevas competencias.",
                "puntaje": 5
            },
            {
                "tipo": "evaluación",
                "pregunta": "¿Cuál es el aspecto más crítico de la transformación descrita?",
                "opciones": [
                    "La velocidad de la automatización",
                    "El impacto en la formación profesional",
                    "La modificación de competencias requeridas"
                ],
                "correcta": 2,
                "explicacion": "El texto enfatiza el cambio en las competencias como aspecto fundamental.",
                "puntaje": 5
            }
        ],
        "tiempo_maximo": 180,
        "puntaje_base": 15
    },
    "nivel_2": {
        "titulo": "Análisis del Cambio Climático",
        "texto_referencia": "texto_cambio_climatico",
        "preguntas": [
            {
                "tipo": "análisis_complejo",
                "pregunta": "¿Cómo se relacionan los sistemas atmosféricos con las actividades antropogénicas según el texto?",
                "opciones": [
                    "No existe relación directa entre ambos",
                    "Los sistemas atmosféricos determinan las actividades humanas",
                    "Existe una interrelación compleja que afecta los modelos predictivos"
                ],
                "correcta": 2,
                "explicacion": "El texto describe una interrelación compleja entre sistemas naturales y actividades humanas.",
                "puntaje": 7
            },
            {
                "tipo": "síntesis",
                "pregunta": "¿Qué conclusión se puede extraer sobre la retroalimentación entre variables ambientales?",
                "opciones": [
                    "Ralentiza el calentamiento global",
                    "Podría acelerar el proceso de calentamiento global",
                    "No afecta al cambio climático"
                ],
                "correcta": 1,
                "explicacion": "El texto indica que la retroalimentación podría acelerar el calentamiento global.",
                "puntaje": 7
            },
            {
                "tipo": "evaluación_crítica",
                "pregunta": "¿Qué desafío principal se presenta para las políticas de mitigación?",
                "opciones": [
                    "La falta de datos científicos",
                    "La complejidad de coordinar acciones a escala global",
                    "El costo económico de las medidas"
                ],
                "correcta": 1,
                "explicacion": "El texto enfatiza el desafío de implementar políticas a escala global.",
                "puntaje": 6
            }
        ],
        "tiempo_maximo": 240,
        "puntaje_base": 20
    }
}

def evaluar_comprension(nivel, respuestas, tiempo_respuesta):
    """
    Evalúa un ejercicio de comprensión.
    
    Args:
        nivel (str): Nivel del ejercicio ('nivel_1', 'nivel_2')
        respuestas (list): Lista de índices de respuestas seleccionadas
        tiempo_respuesta (int): Tiempo total de respuesta en segundos
        
    Returns:
        dict: Resultados de la evaluación
    """
    ejercicio = COMPREHENSION_EXERCISES[nivel]
    correctas = 0
    puntaje_total = 0
    resultados_por_tipo = {
        "análisis": 0,
        "inferencia": 0,
        "evaluación": 0,
        "análisis_complejo": 0,
        "síntesis": 0,
        "evaluación_crítica": 0
    }
    
    for i, (pregunta, respuesta) in enumerate(zip(ejercicio["preguntas"], respuestas)):
        if respuesta == pregunta["correcta"]:
            correctas += 1
            puntaje_total += pregunta["puntaje"]
            resultados_por_tipo[pregunta["tipo"]] += 1
    
    # Factor de tiempo
    factor_tiempo = min(1.0, ejercicio["tiempo_maximo"] / tiempo_respuesta)
    puntaje_final = puntaje_total * factor_tiempo
    
    return {
        "nivel": nivel,
        "correctas": correctas,
        "total": len(ejercicio["preguntas"]),
        "tiempo_respuesta": tiempo_respuesta,
        "tiempo_maximo": ejercicio["tiempo_maximo"],
        "puntaje": puntaje_final,
        "resultados_por_tipo": resultados_por_tipo
    } 