"""
Ejercicios de lectura con diferentes niveles de dificultad.
"""

import random
from datetime import datetime

class EjerciciosLectura:
    def __init__(self):
        self.textos = [
            {
                'id': 1,
                'nivel': 'básico',
                'contenido': 'El sol brillaba intensamente sobre las montañas nevadas, mientras las águilas volaban majestuosamente en círculos sobre el valle verde y frondoso.',
                'palabras_clave': ['sol', 'montañas', 'águilas', 'valle']
            },
            {
                'id': 2,
                'nivel': 'intermedio',
                'contenido': 'La biblioteca estaba en silencio, solo se escuchaba el suave pasar de las páginas y el ocasional suspiro de algún estudiante concentrado en su lectura.',
                'palabras_clave': ['biblioteca', 'silencio', 'páginas', 'estudiante']
            },
            {
                'id': 3,
                'nivel': 'avanzado',
                'contenido': 'En el laboratorio de investigación, los científicos observaban atentamente las reacciones químicas que se producían en los tubos de ensayo, mientras anotaban meticulosamente cada detalle en sus cuadernos.',
                'palabras_clave': ['laboratorio', 'científicos', 'reacciones', 'tubos']
            }
        ]

    def obtener_ejercicio(self, nivel='básico'):
        """Obtiene un ejercicio aleatorio del nivel especificado"""
        ejercicios_nivel = [e for e in self.textos if e['nivel'] == nivel]
        if not ejercicios_nivel:
            ejercicios_nivel = self.textos
        
        ejercicio = random.choice(ejercicios_nivel)
        return {
            'id': ejercicio['id'],
            'texto': ejercicio['contenido'],
            'nivel': ejercicio['nivel'],
            'instrucciones': 'Lee el siguiente texto en voz alta y clara.',
            'tiempo_estimado': len(ejercicio['contenido'].split()) * 0.5  # 0.5 segundos por palabra
        }

    def evaluar_lectura(self, audio_texto, texto_original, tiempo_lectura):
        """
        Evalúa la lectura comparando el texto transcrito con el original
        y analiza el tiempo de lectura
        """
        palabras_original = set(texto_original.lower().split())
        palabras_leidas = set(audio_texto.lower().split())
        
        # Calcular métricas
        palabras_correctas = len(palabras_original.intersection(palabras_leidas))
        palabras_total = len(palabras_original)
        precision = palabras_correctas / palabras_total if palabras_total > 0 else 0
        
        # Calcular velocidad de lectura (palabras por minuto)
        wpm = (len(texto_original.split()) / tiempo_lectura) * 60 if tiempo_lectura > 0 else 0
        
        return {
            'fecha': datetime.utcnow().isoformat(),
            'precision': precision,
            'palabras_por_minuto': wpm,
            'tiempo_total': tiempo_lectura,
            'palabras_correctas': palabras_correctas,
            'palabras_total': palabras_total
        }

    def generar_recomendaciones(self, resultados):
        """Genera recomendaciones basadas en los resultados de la lectura"""
        recomendaciones = []
        
        if resultados['precision'] < 0.8:
            recomendaciones.append("Practica la pronunciación de palabras complejas")
        
        if resultados['palabras_por_minuto'] < 100:
            recomendaciones.append("Realiza ejercicios de velocidad de lectura")
        
        if not recomendaciones:
            recomendaciones.append("¡Buen trabajo! Continúa practicando para mantener tu nivel")
        
        return recomendaciones

READING_EXERCISES = {
    "nivel_1": {
        "titulo": "Impacto de la Inteligencia Artificial en el Mercado Laboral",
        "texto": """La implementación generalizada de sistemas de inteligencia artificial está reconfigurando significativamente el panorama laboral contemporáneo. Las organizaciones están experimentando una transformación fundamental en sus procesos operativos, donde la automatización y los algoritmos de aprendizaje automático están asumiendo tareas tradicionalmente realizadas por humanos. 

Esta evolución tecnológica no solo está modificando los requisitos de competencias profesionales, sino que también está generando nuevos paradigmas en la formación continua y el desarrollo profesional. La adaptabilidad y el aprendizaje permanente se han convertido en competencias fundamentales para la empleabilidad en la era digital.""",
        "palabras_clave": ["automatización", "competencias", "empleabilidad"],
        "tiempo_esperado": 90,
        "puntaje_base": 15,
        "palabras_tecnicas": [
            "inteligencia artificial",
            "algoritmos",
            "automatización",
            "paradigmas"
        ]
    },
    "nivel_2": {
        "titulo": "Cambio Climático: Perspectivas Multidisciplinarias",
        "texto": """El análisis contemporáneo del cambio climático requiere una aproximación multidisciplinaria que integre perspectivas científicas, socioeconómicas y geopolíticas. La interrelación entre los sistemas atmosféricos, los ciclos biogeoquímicos y las actividades antropogénicas presenta una complejidad que desafía los modelos predictivos tradicionales.

Las investigaciones recientes sugieren que la retroalimentación entre diferentes variables ambientales podría acelerar significativamente el proceso de calentamiento global, exacerbando las consecuencias socioeconómicas y generando nuevos desafíos para la implementación de políticas de mitigación y adaptación a escala global.""",
        "palabras_clave": ["biogeoquímicos", "antropogénicas", "retroalimentación"],
        "tiempo_esperado": 120,
        "puntaje_base": 20,
        "palabras_tecnicas": [
            "biogeoquímicos",
            "antropogénicas",
            "retroalimentación",
            "multidisciplinaria"
        ]
    }
}

def evaluar_lectura(nivel, tiempo_total, errores, repeticiones, palabras_tecnicas_correctas):
    """
    Evalúa un ejercicio de lectura.
    
    Args:
        nivel (str): Nivel del ejercicio ('nivel_1', 'nivel_2')
        tiempo_total (int): Tiempo total de lectura en segundos
        errores (int): Número de errores cometidos
        repeticiones (int): Número de repeticiones de palabras
        palabras_tecnicas_correctas (int): Número de palabras técnicas pronunciadas correctamente
        
    Returns:
        dict: Resultados de la evaluación
    """
    ejercicio = READING_EXERCISES[nivel]
    
    # Calcular puntuación por tiempo
    factor_tiempo = min(1.0, ejercicio["tiempo_esperado"] / tiempo_total)
    
    # Calcular puntuación por precisión
    total_palabras_tecnicas = len(ejercicio["palabras_tecnicas"])
    precision_tecnica = palabras_tecnicas_correctas / total_palabras_tecnicas
    
    # Penalización por errores y repeticiones
    penalizacion = (errores * 0.1) + (repeticiones * 0.05)
    
    # Calcular puntaje final
    puntaje_base = ejercicio["puntaje_base"]
    puntaje = puntaje_base * (factor_tiempo * 0.4 + precision_tecnica * 0.6 - penalizacion)
    puntaje = max(0, puntaje)  # Asegurar que no sea negativo
    
    return {
        "nivel": nivel,
        "tiempo_total": tiempo_total,
        "tiempo_esperado": ejercicio["tiempo_esperado"],
        "errores": errores,
        "repeticiones": repeticiones,
        "palabras_tecnicas_correctas": palabras_tecnicas_correctas,
        "palabras_tecnicas_total": total_palabras_tecnicas,
        "puntaje": puntaje
    } 