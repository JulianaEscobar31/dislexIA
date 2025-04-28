from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename
import speech_recognition as sr
from pydub import AudioSegment
import numpy as np
import soundfile as sf
import tempfile
import random
from .servicios.servicio_ejercicios import ServicioEjercicios
from .servicios.servicio_audio import ServicioAudio
from .servicios.servicio_ml import ServicioML
from .servicios.servicio_evaluacion import ServicioEvaluacion
from .ejercicios.ejercicios_lectura import EjerciciosLectura
from .ejercicios.ejercicios_dictado import EjerciciosDictado
from .ejercicios.ejercicios_comprension import EjerciciosComprension
from .ejercicios.evaluador import Evaluador
from .database import db

rutas = Blueprint('rutas', __name__)

# Textos de ejemplo para la lectura
TEXTOS_EJEMPLO = [
    "El sol brillaba intensamente sobre las montañas nevadas, mientras las águilas volaban majestuosamente en círculos sobre el valle verde y frondoso.",
    "La biblioteca estaba en silencio, solo se escuchaba el suave pasar de las páginas y el ocasional suspiro de algún estudiante concentrado.",
    "En el mercado local, los vendedores pregonaban sus productos frescos, creando una sinfonía de voces y aromas que llenaban el aire.",
]

ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@rutas.route('/api/texto-ejemplo', methods=['GET'])
def obtener_texto_ejemplo():
    """Endpoint para obtener un texto aleatorio para el ejercicio de lectura"""
    texto = random.choice(TEXTOS_EJEMPLO)
    return jsonify({
        'texto': texto,
        'instrucciones': 'Por favor, lea el siguiente texto en voz alta y clara:'
    })

@rutas.route('/api/audio/procesar', methods=['POST'])
def procesar_audio():
    """Endpoint para procesar archivos de audio"""
    if 'audio' not in request.files:
        return jsonify({'error': 'No se encontró el archivo de audio'}), 400
    
    audio_file = request.files['audio']
    if audio_file.filename == '':
        return jsonify({'error': 'No se seleccionó ningún archivo'}), 400
    
    if not allowed_file(audio_file.filename):
        return jsonify({'error': 'Tipo de archivo no permitido'}), 400

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            audio_file.save(temp_file.name)
            data, sample_rate = sf.read(temp_file.name)
            duration = len(data) / sample_rate
            intensity = np.abs(data).mean()
            
            recognizer = sr.Recognizer()
            with sr.AudioFile(temp_file.name) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data, language='es-ES')
            
            words = len(text.split())
            wpm = (words / duration) * 60
            os.unlink(temp_file.name)

            return jsonify({
                'texto': text,
                'duracion': duration,
                'palabras_por_minuto': wpm,
                'intensidad': float(intensity),
                'palabras_totales': words
            })
    
    except Exception as e:
        if 'temp_file' in locals():
            try:
                os.unlink(temp_file.name)
            except:
                pass
        return jsonify({'error': str(e)}), 500

@rutas.route('/api/health', methods=['GET'])
def health_check():
    """Endpoint para verificar el estado del servicio"""
    return jsonify({'estado': 'ok'}) 