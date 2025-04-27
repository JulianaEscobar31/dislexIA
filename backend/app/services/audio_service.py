import speech_recognition as sr
from pydub import AudioSegment
import os
import logging
from typing import Dict, Any

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class AudioService:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        
    def procesar_audio(self, audio_path: str) -> Dict[Any, Any]:
        """
        Procesa un archivo de audio para extraer métricas y transcripción
        """
        try:
            logger.info(f"Iniciando procesamiento de audio: {audio_path}")
            
            # Verificar que el archivo existe
            if not os.path.exists(audio_path):
                logger.error(f"Archivo no encontrado: {audio_path}")
                return {"error": "Archivo de audio no encontrado"}

            # Convertir audio a formato WAV si es necesario
            try:
                audio = AudioSegment.from_file(audio_path)
                wav_path = audio_path.rsplit('.', 1)[0] + '.wav'
                audio.export(wav_path, format="wav")
                logger.info(f"Audio convertido a WAV: {wav_path}")
            except Exception as e:
                logger.error(f"Error al convertir audio: {str(e)}")
                return {"error": f"Error al convertir audio: {str(e)}"}

            # Realizar transcripción
            try:
                with sr.AudioFile(wav_path) as source:
                    audio_data = self.recognizer.record(source)
                    texto = self.recognizer.recognize_google(audio_data, language='es-ES')
                    logger.info("Transcripción completada")
            except sr.UnknownValueError:
                logger.error("No se pudo entender el audio")
                return {"error": "No se pudo entender el audio"}
            except sr.RequestError as e:
                logger.error(f"Error en el servicio de reconocimiento: {str(e)}")
                return {"error": f"Error en el servicio de reconocimiento: {str(e)}"}

            # Calcular métricas
            duracion = len(audio) / 1000.0  # convertir a segundos
            intensidad_promedio = float(audio.dBFS)
            numero_pausas = len([1 for i in range(1, len(audio) - 1) if 
                               audio[i].dBFS < -30 and 
                               audio[i-1].dBFS > -30 and 
                               audio[i+1].dBFS > -30])

            # Calcular fluidez (métrica simple basada en pausas/duración)
            fluidez = 1.0 - (numero_pausas / (duracion / 5))  # normalizado a 1
            fluidez = max(0.0, min(1.0, fluidez))  # mantener entre 0 y 1

            logger.info("Análisis de audio completado")
            
            # Limpiar archivos temporales
            try:
                os.remove(wav_path)
                logger.info("Archivos temporales eliminados")
            except Exception as e:
                logger.warning(f"Error al eliminar archivo temporal: {str(e)}")

            return {
                "texto_transcrito": texto,
                "metricas": {
                    "duracion": duracion,
                    "intensidad_promedio": intensidad_promedio,
                    "numero_pausas": numero_pausas,
                    "fluidez": fluidez
                }
            }

        except Exception as e:
            logger.error(f"Error general en el procesamiento de audio: {str(e)}")
            return {"error": f"Error general en el procesamiento de audio: {str(e)}"}

audio_service = AudioService() 