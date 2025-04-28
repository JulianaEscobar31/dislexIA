"""
Módulo principal para la evaluación de ejercicios de dislexia.
"""

from .ejercicios_dictado import evaluar_dictado, DICTATION_EXERCISES
from .ejercicios_lectura import evaluar_lectura, READING_EXERCISES
from .ejercicios_comprension import evaluar_comprension, COMPREHENSION_EXERCISES

class Evaluador:
    @staticmethod
    def evaluar_ejercicio_dictado(nivel, respuestas):
        """
        Evalúa un ejercicio de dictado.
        """
        return evaluar_dictado(nivel, respuestas)

    @staticmethod
    def evaluar_ejercicio_lectura(nivel, tiempo_total, errores, repeticiones, palabras_tecnicas_correctas):
        """
        Evalúa un ejercicio de lectura.
        """
        return evaluar_lectura(nivel, tiempo_total, errores, repeticiones, palabras_tecnicas_correctas)

    @staticmethod
    def evaluar_ejercicio_comprension(nivel, respuestas, tiempo_respuesta):
        """
        Evalúa un ejercicio de comprensión.
        """
        return evaluar_comprension(nivel, respuestas, tiempo_respuesta)

    @staticmethod
    def obtener_ejercicios_dictado():
        """
        Obtiene todos los ejercicios de dictado disponibles.
        """
        return DICTATION_EXERCISES

    @staticmethod
    def obtener_ejercicios_lectura():
        """
        Obtiene todos los ejercicios de lectura disponibles.
        """
        return READING_EXERCISES

    @staticmethod
    def obtener_ejercicios_comprension():
        """
        Obtiene todos los ejercicios de comprensión disponibles.
        """
        return COMPREHENSION_EXERCISES

def obtener_ejercicios():
    """
    Obtiene todos los ejercicios disponibles.
    
    Returns:
        dict: Diccionario con todos los ejercicios
    """
    return {
        "dictado": DICTATION_EXERCISES,
        "lectura": READING_EXERCISES,
        "comprension": COMPREHENSION_EXERCISES
    }

def evaluar_ejercicios(resultados):
    """
    Evalúa todos los ejercicios realizados.
    
    Args:
        resultados (dict): Diccionario con los resultados de todos los ejercicios
        
    Returns:
        dict: Resultados de la evaluación completa
    """
    evaluacion = {
        "dictado": [],
        "lectura": [],
        "comprension": [],
        "metricas_generales": {},
        "indicadores_dislexia": {}
    }
    
    # Evaluar ejercicios de dictado
    for ejercicio in resultados["ejercicios_dictado"]:
        eval_dictado = evaluar_dictado(
            ejercicio["nivel"],
            ejercicio["respuestas"]
        )
        evaluacion["dictado"].append(eval_dictado)
    
    # Evaluar ejercicios de lectura
    for ejercicio in resultados["ejercicios_lectura"]:
        eval_lectura = evaluar_lectura(
            ejercicio["nivel"],
            ejercicio["tiempo_total"],
            ejercicio["errores"],
            ejercicio["repeticiones"],
            ejercicio["palabras_tecnicas_correctas"]
        )
        evaluacion["lectura"].append(eval_lectura)
    
    # Evaluar ejercicios de comprensión
    for ejercicio in resultados["ejercicios_comprension"]:
        eval_comprension = evaluar_comprension(
            ejercicio["nivel"],
            ejercicio["respuestas"],
            ejercicio["tiempo_respuesta"]
        )
        evaluacion["comprension"].append(eval_comprension)
    
    # Calcular métricas generales
    evaluacion["metricas_generales"] = calcular_metricas_generales(evaluacion)
    
    # Calcular indicadores de dislexia
    evaluacion["indicadores_dislexia"] = calcular_indicadores_dislexia(evaluacion)
    
    return evaluacion

def calcular_metricas_generales(evaluacion):
    """
    Calcula métricas generales basadas en todos los ejercicios.
    
    Args:
        evaluacion (dict): Resultados de todos los ejercicios
        
    Returns:
        dict: Métricas generales
    """
    # Calcular promedios de puntajes
    puntaje_dictado = sum(e["puntaje"] for e in evaluacion["dictado"]) / len(evaluacion["dictado"])
    puntaje_lectura = sum(e["puntaje"] for e in evaluacion["lectura"]) / len(evaluacion["lectura"])
    puntaje_comprension = sum(e["puntaje"] for e in evaluacion["comprension"]) / len(evaluacion["comprension"])
    
    # Calcular totales de errores
    total_errores_dictado = sum(len(e["errores"]) for e in evaluacion["dictado"])
    total_errores_lectura = sum(e["errores"] for e in evaluacion["lectura"])
    
    # Calcular promedios de tiempo
    tiempo_promedio_lectura = sum(e["tiempo_total"] for e in evaluacion["lectura"]) / len(evaluacion["lectura"])
    tiempo_promedio_comprension = sum(e["tiempo_respuesta"] for e in evaluacion["comprension"]) / len(evaluacion["comprension"])
    
    return {
        "puntajes": {
            "dictado": puntaje_dictado,
            "lectura": puntaje_lectura,
            "comprension": puntaje_comprension,
            "total": (puntaje_dictado + puntaje_lectura + puntaje_comprension) / 3
        },
        "errores": {
            "dictado": total_errores_dictado,
            "lectura": total_errores_lectura
        },
        "tiempos": {
            "lectura": tiempo_promedio_lectura,
            "comprension": tiempo_promedio_comprension
        }
    }

def calcular_indicadores_dislexia(evaluacion):
    """
    Calcula indicadores específicos de dislexia basados en los resultados.
    
    Args:
        evaluacion (dict): Resultados de todos los ejercicios
        
    Returns:
        dict: Indicadores de dislexia
    """
    metricas = evaluacion["metricas_generales"]
    
    # Calcular indicadores específicos
    indicadores = {
        "dificultad_lectura": calcular_dificultad_lectura(evaluacion["lectura"]),
        "dificultad_escritura": calcular_dificultad_escritura(evaluacion["dictado"]),
        "dificultad_comprension": calcular_dificultad_comprension(evaluacion["comprension"]),
        "patron_errores": analizar_patron_errores(evaluacion)
    }
    
    # Calcular probabilidad general de dislexia
    probabilidad = calcular_probabilidad_dislexia(indicadores, metricas)
    indicadores["probabilidad_dislexia"] = probabilidad
    
    return indicadores

def calcular_dificultad_lectura(resultados_lectura):
    """Calcula el nivel de dificultad en lectura."""
    total_tiempo = sum(r["tiempo_total"] for r in resultados_lectura)
    total_errores = sum(r["errores"] for r in resultados_lectura)
    total_repeticiones = sum(r["repeticiones"] for r in resultados_lectura)
    
    factor_tiempo = sum(r["tiempo_total"] / r["tiempo_esperado"] for r in resultados_lectura) / len(resultados_lectura)
    factor_errores = total_errores / len(resultados_lectura)
    factor_repeticiones = total_repeticiones / len(resultados_lectura)
    
    return (factor_tiempo * 0.4 + factor_errores * 0.3 + factor_repeticiones * 0.3)

def calcular_dificultad_escritura(resultados_dictado):
    """Calcula el nivel de dificultad en escritura."""
    total_errores = sum(len(r["errores"]) for r in resultados_dictado)
    promedio_errores = total_errores / len(resultados_dictado)
    
    tipos_errores = {
        "acentuación": 0,
        "orden_letras": 0,
        "omisión_adición": 0,
        "múltiple": 0
    }
    
    for resultado in resultados_dictado:
        for error in resultado["errores"]:
            tipos_errores[error["tipo_error"]] += 1
    
    return {
        "nivel": promedio_errores / 7,  # 7 palabras por ejercicio
        "tipos_errores": tipos_errores
    }

def calcular_dificultad_comprension(resultados_comprension):
    """Calcula el nivel de dificultad en comprensión."""
    promedio_correctas = sum(r["correctas"] / r["total"] for r in resultados_comprension) / len(resultados_comprension)
    promedio_tiempo = sum(r["tiempo_respuesta"] / r["tiempo_maximo"] for r in resultados_comprension) / len(resultados_comprension)
    
    return {
        "precision": 1 - promedio_correctas,
        "velocidad": promedio_tiempo
    }

def analizar_patron_errores(evaluacion):
    """Analiza patrones específicos en los errores cometidos."""
    patrones = {
        "confusion_letras": 0,
        "omision_letras": 0,
        "inversion_orden": 0,
        "errores_acentuacion": 0
    }
    
    # Analizar errores de dictado
    for resultado in evaluacion["dictado"]:
        for error in resultado["errores"]:
            if error["tipo_error"] == "orden_letras":
                patrones["inversion_orden"] += 1
            elif error["tipo_error"] == "omisión_adición":
                patrones["omision_letras"] += 1
            elif error["tipo_error"] == "acentuación":
                patrones["errores_acentuacion"] += 1
    
    return patrones

def calcular_probabilidad_dislexia(indicadores, metricas):
    """
    Calcula la probabilidad general de dislexia basada en todos los indicadores.
    
    Esta función utiliza un sistema de ponderación para diferentes factores:
    - Dificultad en lectura: 35%
    - Dificultad en escritura: 35%
    - Dificultad en comprensión: 20%
    - Patrones específicos: 10%
    """
    # Pesos para cada factor
    pesos = {
        "lectura": 0.35,
        "escritura": 0.35,
        "comprension": 0.20,
        "patrones": 0.10
    }
    
    # Calcular probabilidad por área
    prob_lectura = indicadores["dificultad_lectura"]
    prob_escritura = indicadores["dificultad_escritura"]["nivel"]
    prob_comprension = (indicadores["dificultad_comprension"]["precision"] + 
                       indicadores["dificultad_comprension"]["velocidad"]) / 2
    
    # Calcular factor de patrones específicos
    total_patrones = sum(indicadores["patron_errores"].values())
    factor_patrones = min(1.0, total_patrones / 10)  # Normalizar a máximo 1.0
    
    # Calcular probabilidad final ponderada
    probabilidad = (
        prob_lectura * pesos["lectura"] +
        prob_escritura * pesos["escritura"] +
        prob_comprension * pesos["comprension"] +
        factor_patrones * pesos["patrones"]
    )
    
    return min(1.0, probabilidad)  # Asegurar que no exceda 1.0 