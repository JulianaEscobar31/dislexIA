"""
Ejercicios de lectura con diferentes niveles de dificultad.
"""

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