from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from ..ml.models import DislexiaModel
import difflib

router = APIRouter()
modelo_dislexia = DislexiaModel()

class ResultadoLectura(BaseModel):
    tiempo_total: float
    errores: int
    pausas: int
    repeticiones: int
    texto_leido: str

class ResultadoDictado(BaseModel):
    tiempo_escritura: float
    errores_ortograficos: int
    correcciones: int
    texto_original: str
    texto_escrito: str

class ResultadoEvaluacion(BaseModel):
    probabilidad_dislexia: float
    nivel_confianza: float
    recomendaciones: List[str]
    metricas_detalladas: dict

@router.post("/evaluar/lectura", response_model=ResultadoEvaluacion)
async def evaluar_lectura(resultado: ResultadoLectura):
    try:
        features = modelo_dislexia.procesar_datos_lectura(
            resultado.tiempo_total,
            resultado.errores,
            resultado.pausas,
            resultado.repeticiones
        )
        
        prediccion = modelo_dislexia.predecir_dislexia(features, tipo_ejercicio='lectura')
        
        metricas = {
            'tiempo_por_palabra': resultado.tiempo_total / len(resultado.texto_leido.split()),
            'tasa_errores': resultado.errores / max(resultado.tiempo_total, 1),
            'tasa_pausas': resultado.pausas / max(resultado.tiempo_total, 1),
            'tasa_repeticiones': resultado.repeticiones / max(resultado.tiempo_total, 1)
        }
        
        recomendaciones = generar_recomendaciones_lectura(prediccion['probabilidad_dislexia'], metricas)
        
        return ResultadoEvaluacion(
            probabilidad_dislexia=prediccion['probabilidad_dislexia'],
            nivel_confianza=prediccion['nivel_confianza'],
            recomendaciones=recomendaciones,
            metricas_detalladas=metricas
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/evaluar/dictado", response_model=ResultadoEvaluacion)
async def evaluar_dictado(resultado: ResultadoDictado):
    try:
        # Calcular métricas adicionales para dictado
        palabras_original = len(resultado.texto_original.split())
        palabras_escritas = len(resultado.texto_escrito.split())
        palabras_correctas = sum(1 for a, b in zip(resultado.texto_original.split(), resultado.texto_escrito.split()) if a == b)
        
        # Calcular similitud de secuencia
        matcher = difflib.SequenceMatcher(None, resultado.texto_original, resultado.texto_escrito)
        similitud = matcher.ratio()
        
        features = modelo_dislexia.procesar_datos_dictado(
            resultado.tiempo_escritura,
            resultado.errores_ortograficos,
            resultado.correcciones,
            resultado.texto_original,
            resultado.texto_escrito
        )
        
        prediccion = modelo_dislexia.predecir_dislexia(features, tipo_ejercicio='dictado')
        
        metricas = {
            'tiempo_por_palabra': resultado.tiempo_escritura / max(palabras_escritas, 1),
            'precisión_palabras': palabras_correctas / max(palabras_original, 1),
            'tasa_errores': resultado.errores_ortograficos / max(palabras_escritas, 1),
            'tasa_correcciones': resultado.correcciones / max(resultado.tiempo_escritura, 1),
            'similitud_texto': similitud,
            'diferencia_longitud': abs(palabras_original - palabras_escritas) / max(palabras_original, 1)
        }
        
        recomendaciones = generar_recomendaciones_dictado(prediccion['probabilidad_dislexia'], metricas)
        
        return ResultadoEvaluacion(
            probabilidad_dislexia=prediccion['probabilidad_dislexia'],
            nivel_confianza=prediccion['nivel_confianza'],
            recomendaciones=recomendaciones,
            metricas_detalladas=metricas
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def generar_recomendaciones_lectura(probabilidad: float, metricas: dict) -> List[str]:
    recomendaciones = []
    
    if probabilidad > 0.7:
        recomendaciones.extend([
            "Se recomienda una evaluación profesional detallada",
            "Practicar ejercicios de segmentación fonológica",
            "Utilizar materiales de lectura con formato adaptado"
        ])
    elif probabilidad > 0.4:
        recomendaciones.extend([
            "Continuar practicando la lectura con textos graduales",
            "Realizar ejercicios de comprensión lectora",
            "Considerar una evaluación de seguimiento"
        ])
    else:
        recomendaciones.extend([
            "Mantener la práctica regular de lectura",
            "Explorar diferentes tipos de textos",
            "Realizar ejercicios de velocidad lectora"
        ])
    
    # Recomendaciones basadas en métricas específicas
    if metricas['tasa_errores'] > 0.1:
        recomendaciones.append("Enfocarse en la precisión de la lectura")
    if metricas['tasa_pausas'] > 0.2:
        recomendaciones.append("Practicar la fluidez lectora")
    if metricas['tasa_repeticiones'] > 0.15:
        recomendaciones.append("Trabajar en la confianza al leer")
    
    return recomendaciones

def generar_recomendaciones_dictado(probabilidad: float, metricas: dict) -> List[str]:
    recomendaciones = []
    
    if probabilidad > 0.7:
        recomendaciones.extend([
            "Se sugiere apoyo especializado en escritura",
            "Practicar ejercicios de conciencia fonológica",
            "Utilizar herramientas de corrección ortográfica"
        ])
    elif probabilidad > 0.4:
        recomendaciones.extend([
            "Realizar ejercicios de escritura guiada",
            "Practicar la escritura de palabras frecuentes",
            "Considerar ejercicios de memoria visual"
        ])
    else:
        recomendaciones.extend([
            "Continuar con prácticas regulares de escritura",
            "Explorar diferentes tipos de ejercicios de dictado",
            "Mantener un diario de escritura"
        ])
    
    # Recomendaciones basadas en métricas específicas
    if metricas['precisión_palabras'] < 0.8:
        recomendaciones.append("Enfocarse en la precisión ortográfica")
    if metricas['tasa_errores'] > 0.15:
        recomendaciones.append("Practicar la escritura de palabras problemáticas")
    if metricas['tasa_correcciones'] > 0.2:
        recomendaciones.append("Trabajar en la planificación antes de escribir")
    if metricas['diferencia_longitud'] > 0.2:
        recomendaciones.append("Prestar atención a la estructura de las oraciones")
    
    return recomendaciones 