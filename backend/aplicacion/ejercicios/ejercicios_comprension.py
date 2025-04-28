"""
Ejercicios de comprensión con diferentes niveles de dificultad.
"""

import random
from datetime import datetime

class EjerciciosComprension:
    def __init__(self):
        self.ejercicios = [
            {
                'id': 1,
                'nivel': 'básico',
                'texto': 'Juan tiene un jardín lleno de flores coloridas. Todas las mañanas riega las plantas y quita las malas hierbas. Las mariposas y abejas visitan frecuentemente su jardín para recoger el néctar de las flores.',
                'preguntas': [
                    {
                        'pregunta': '¿Qué hace Juan todas las mañanas?',
                        'opciones': ['Riega las plantas', 'Poda los árboles', 'Planta nuevas flores', 'Pinta las flores'],
                        'respuesta_correcta': 0
                    },
                    {
                        'pregunta': '¿Qué animales visitan el jardín?',
                        'opciones': ['Pájaros y gatos', 'Mariposas y abejas', 'Hormigas y arañas', 'Lagartijas y ranas'],
                        'respuesta_correcta': 1
                    }
                ]
            },
            {
                'id': 2,
                'nivel': 'intermedio',
                'texto': 'La contaminación del aire es un problema grave en las grandes ciudades. Los automóviles y las fábricas emiten gases tóxicos que dañan la atmósfera. Para combatir este problema, muchas ciudades están promoviendo el uso de transporte público y energías renovables.',
                'preguntas': [
                    {
                        'pregunta': '¿Cuál es el principal problema mencionado en el texto?',
                        'opciones': ['La contaminación del agua', 'La contaminación del aire', 'La deforestación', 'El cambio climático'],
                        'respuesta_correcta': 1
                    },
                    {
                        'pregunta': '¿Qué soluciones se proponen?',
                        'opciones': ['Cerrar todas las fábricas', 'Prohibir los automóviles', 'Usar transporte público y energías renovables', 'Construir más carreteras'],
                        'respuesta_correcta': 2
                    }
                ]
            }
        ]

    def obtener_ejercicio(self, nivel='básico'):
        """Obtiene un ejercicio de comprensión lectora aleatorio del nivel especificado"""
        ejercicios_nivel = [e for e in self.ejercicios if e['nivel'] == nivel]
        if not ejercicios_nivel:
            ejercicios_nivel = self.ejercicios
        
        ejercicio = random.choice(ejercicios_nivel)
        return {
            'id': ejercicio['id'],
            'texto': ejercicio['texto'],
            'nivel': ejercicio['nivel'],
            'preguntas': [{'pregunta': p['pregunta'], 'opciones': p['opciones']} for p in ejercicio['preguntas']],
            'instrucciones': 'Lee el texto con atención y responde las siguientes preguntas.',
            'tiempo_estimado': len(ejercicio['texto'].split()) * 1.5  # 1.5 segundos por palabra
        }

    def evaluar_comprension(self, id_ejercicio, respuestas_usuario):
        """
        Evalúa las respuestas del usuario para un ejercicio de comprensión
        """
        ejercicio = next((e for e in self.ejercicios if e['id'] == id_ejercicio), None)
        if not ejercicio:
            raise ValueError('Ejercicio no encontrado')
        
        total_preguntas = len(ejercicio['preguntas'])
        respuestas_correctas = sum(
            1 for i, respuesta in enumerate(respuestas_usuario)
            if i < total_preguntas and respuesta == ejercicio['preguntas'][i]['respuesta_correcta']
        )
        
        porcentaje = (respuestas_correctas / total_preguntas) * 100 if total_preguntas > 0 else 0
        
        return {
            'fecha': datetime.utcnow().isoformat(),
            'total_preguntas': total_preguntas,
            'respuestas_correctas': respuestas_correctas,
            'porcentaje': porcentaje,
            'nivel': ejercicio['nivel']
        }

    def generar_recomendaciones(self, resultados):
        """Genera recomendaciones basadas en los resultados de comprensión"""
        recomendaciones = []
        
        if resultados['porcentaje'] < 60:
            recomendaciones.append("Practica la lectura detenida y toma notas mientras lees")
            recomendaciones.append("Intenta identificar las ideas principales del texto")
        elif resultados['porcentaje'] < 80:
            recomendaciones.append("Mejora tu comprensión prestando atención a los detalles")
        
        if not recomendaciones:
            recomendaciones.append("¡Excelente comprensión lectora! Continúa con ejercicios más desafiantes")
        
        return recomendaciones

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