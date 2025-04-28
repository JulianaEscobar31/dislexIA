"""
Ejercicios de dictado con diferentes niveles de dificultad.
"""

import random
from datetime import datetime
import difflib

class EjerciciosDictado:
    def __init__(self):
        self.frases = [
            {
                'id': 1,
                'nivel': 'básico',
                'contenido': 'El perro juega en el parque con su pelota roja.',
                'palabras_dificiles': ['perro', 'parque', 'pelota']
            },
            {
                'id': 2,
                'nivel': 'intermedio',
                'contenido': 'La mariposa multicolor volaba graciosamente entre las flores del jardín.',
                'palabras_dificiles': ['mariposa', 'multicolor', 'graciosamente']
            },
            {
                'id': 3,
                'nivel': 'avanzado',
                'contenido': 'El científico explicó detalladamente el experimento sobre la fotosíntesis en las plantas.',
                'palabras_dificiles': ['científico', 'experimento', 'fotosíntesis']
            }
        ]

    def obtener_ejercicio(self, nivel='básico'):
        """Obtiene un ejercicio de dictado aleatorio del nivel especificado"""
        ejercicios_nivel = [e for e in self.frases if e['nivel'] == nivel]
        if not ejercicios_nivel:
            ejercicios_nivel = self.frases
        
        ejercicio = random.choice(ejercicios_nivel)
        return {
            'id': ejercicio['id'],
            'nivel': ejercicio['nivel'],
            'instrucciones': 'Escucha atentamente y escribe el texto que se te dicta.',
            'duracion_estimada': len(ejercicio['contenido'].split()) * 2  # 2 segundos por palabra
        }

    def evaluar_dictado(self, texto_usuario, texto_original):
        """
        Evalúa el dictado comparando el texto escrito por el usuario
        con el texto original
        """
        # Normalizar textos
        texto_usuario = texto_usuario.lower().strip()
        texto_original = texto_original.lower().strip()
        
        # Calcular similitud
        matcher = difflib.SequenceMatcher(None, texto_usuario, texto_original)
        similitud = matcher.ratio()
        
        # Contar errores ortográficos
        palabras_usuario = texto_usuario.split()
        palabras_original = texto_original.split()
        errores = sum(1 for i in range(min(len(palabras_usuario), len(palabras_original)))
                     if palabras_usuario[i] != palabras_original[i])
        
        return {
            'fecha': datetime.utcnow().isoformat(),
            'similitud': similitud,
            'errores_ortograficos': errores,
            'longitud_texto': len(palabras_original),
            'palabras_correctas': len(palabras_original) - errores
        }

    def generar_recomendaciones(self, resultados):
        """Genera recomendaciones basadas en los resultados del dictado"""
        recomendaciones = []
        
        if resultados['similitud'] < 0.8:
            recomendaciones.append("Practica la escucha activa y la atención al detalle")
        
        if resultados['errores_ortograficos'] > 3:
            recomendaciones.append("Repasa las reglas ortográficas básicas")
        
        if not recomendaciones:
            recomendaciones.append("¡Excelente trabajo! Sigue practicando para mantener tu nivel")
        
        return recomendaciones

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