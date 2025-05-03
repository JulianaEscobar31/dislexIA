"""
Ejercicios de comprensión con diferentes niveles de dificultad.
"""

import random
from datetime import datetime

TEXTOS_REFERENCIA = {
    "texto_ia_mercado_laboral": """
    La inteligencia artificial está transformando el mercado laboral de manera significativa. 
    La automatización de tareas rutinarias ha llevado a una redefinición de las competencias profesionales. 
    Las habilidades técnicas siguen siendo importantes, pero ahora se valora más la capacidad de adaptación 
    y el aprendizaje continuo. Los profesionales deben estar preparados para actualizar constantemente 
    sus conocimientos y desarrollar nuevas habilidades que complementen las capacidades de la IA.
    """,
    
    "texto_cambio_climatico": """
    El cambio climático es uno de los desafíos más complejos que enfrenta la humanidad. 
    Los sistemas atmosféricos interactúan con las actividades humanas de manera no lineal, 
    creando patrones de retroalimentación que pueden acelerar el calentamiento global. 
    La implementación de políticas efectivas requiere una coordinación global sin precedentes 
    y una comprensión profunda de las interacciones entre sistemas naturales y sociales.
    """,
    
    "texto_historia_tecnologia": """
    La evolución de la tecnología ha sido un proceso continuo de innovación y adaptación. 
    Desde la invención de la rueda hasta la era digital, cada avance tecnológico ha transformado 
    la forma en que los seres humanos interactúan con su entorno. La revolución digital actual 
    está redefiniendo conceptos fundamentales como la privacidad, la comunicación y el trabajo.
    """,
    
    "texto_ecosistema_marino": """
    Los ecosistemas marinos son sistemas complejos donde múltiples especies interactúan 
    en un delicado equilibrio. La sobrepesca y la contaminación han alterado significativamente 
    estos ecosistemas, afectando no solo a las especies marinas sino también a las comunidades 
    costeras que dependen de ellos. La conservación de estos ecosistemas requiere un enfoque 
    integrado que considere tanto factores biológicos como socioeconómicos.
    """
}

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
    },
    "nivel_3": {
        "titulo": "Evolución Tecnológica y Sociedad",
        "texto_referencia": "texto_historia_tecnologia",
        "preguntas": [
            {
                "tipo": "análisis_complejo",
                "pregunta": "¿Cómo ha evolucionado la relación entre tecnología y sociedad según el texto?",
                "opciones": [
                    "Ha sido un proceso lineal y predecible",
                    "Ha generado cambios profundos en la interacción humana",
                    "Ha mantenido los mismos patrones a lo largo de la historia"
                ],
                "correcta": 1,
                "explicacion": "El texto describe una transformación continua que afecta aspectos fundamentales de la sociedad.",
                "puntaje": 8
            },
            {
                "tipo": "síntesis",
                "pregunta": "¿Qué caracteriza a la revolución digital actual según el texto?",
                "opciones": [
                    "Su impacto en la privacidad y la comunicación",
                    "Su similitud con revoluciones tecnológicas anteriores",
                    "Su enfoque exclusivo en aspectos técnicos"
                ],
                "correcta": 0,
                "explicacion": "El texto destaca la redefinición de conceptos fundamentales como la privacidad y la comunicación.",
                "puntaje": 8
            },
            {
                "tipo": "evaluación_crítica",
                "pregunta": "¿Qué implica la continuidad del proceso de innovación tecnológica?",
                "opciones": [
                    "Una estabilización de los cambios sociales",
                    "Una adaptación constante de la sociedad",
                    "Una reducción de la importancia de la tecnología"
                ],
                "correcta": 1,
                "explicacion": "El texto sugiere que la innovación tecnológica requiere una adaptación constante de la sociedad.",
                "puntaje": 8
            }
        ],
        "tiempo_maximo": 300,
        "puntaje_base": 24
    }
}

def obtener_ejercicio(nivel='nivel_1'):
    """
    Obtiene un ejercicio de comprensión lectora del nivel especificado.
    
    Args:
        nivel (str): Nivel del ejercicio ('nivel_1', 'nivel_2', 'nivel_3')
        
    Returns:
        dict: Ejercicio con texto y preguntas
    """
    ejercicio = COMPREHENSION_EXERCISES[nivel]
    texto = TEXTOS_REFERENCIA[ejercicio["texto_referencia"]]
    
    return {
        "id": nivel,
        "titulo": ejercicio["titulo"],
        "texto": texto,
        "nivel": nivel,
        "preguntas": [{"pregunta": p["pregunta"], "opciones": p["opciones"]} for p in ejercicio["preguntas"]],
        "instrucciones": "Lee el texto con atención y responde las siguientes preguntas.",
        "tiempo_estimado": ejercicio["tiempo_maximo"]
    }

def evaluar_comprension(nivel, respuestas, tiempo_respuesta):
    """
    Evalúa un ejercicio de comprensión.
    
    Args:
        nivel (str): Nivel del ejercicio ('nivel_1', 'nivel_2', 'nivel_3')
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
    total_preguntas = len(ejercicio["preguntas"])
    if total_preguntas == 0:
        return {
            "nivel": nivel,
            "correctas": 0,
            "total": 0,
            "tiempo_respuesta": tiempo_respuesta,
            "tiempo_maximo": ejercicio["tiempo_maximo"],
            "puntaje": 0,
            "resultados_por_tipo": resultados_por_tipo,
            "recomendaciones": ["No se encontraron preguntas para este ejercicio. Intenta con otro nivel o contacta al administrador."]
        }
    for i, (pregunta, respuesta) in enumerate(zip(ejercicio["preguntas"], respuestas)):
        if respuesta == pregunta["correcta"]:
            correctas += 1
            puntaje_total += pregunta["puntaje"]
            resultados_por_tipo[pregunta["tipo"]] += 1
    # Factor de tiempo
    factor_tiempo = min(1.0, ejercicio["tiempo_maximo"] / tiempo_respuesta) if tiempo_respuesta > 0 else 1.0
    puntaje_final = puntaje_total * factor_tiempo
    # Generar recomendaciones
    recomendaciones = []
    if puntaje_final < ejercicio["puntaje_base"] * 0.6:
        recomendaciones.append("Practica la lectura detenida y toma notas mientras lees")
        recomendaciones.append("Intenta identificar las ideas principales del texto")
    elif puntaje_final < ejercicio["puntaje_base"] * 0.8:
        recomendaciones.append("Mejora tu comprensión prestando atención a los detalles")
        recomendaciones.append("Intenta relacionar las ideas principales con los detalles del texto")
    else:
        recomendaciones.append("¡Excelente comprensión lectora! Continúa con ejercicios más desafiantes")
    return {
        "nivel": nivel,
        "correctas": correctas,
        "total": total_preguntas,
        "tiempo_respuesta": tiempo_respuesta,
        "tiempo_maximo": ejercicio["tiempo_maximo"],
        "puntaje": puntaje_final,
        "resultados_por_tipo": resultados_por_tipo,
        "recomendaciones": recomendaciones
    } 