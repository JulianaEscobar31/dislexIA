from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename
import speech_recognition as sr
from pydub import AudioSegment
import numpy as np
from app import db
import soundfile as sf
import tempfile
import random

bp = Blueprint('main', __name__)

# Textos de ejemplo para la lectura
TEXTOS_EJEMPLO = [
    "El sol brillaba intensamente sobre las montañas nevadas, mientras las águilas volaban majestuosamente en círculos sobre el valle verde y frondoso.",
    "La biblioteca estaba en silencio, solo se escuchaba el suave pasar de las páginas y el ocasional suspiro de algún estudiante concentrado.",
    "En el mercado local, los vendedores pregonaban sus productos frescos, creando una sinfonía de voces y aromas que llenaban el aire.",
]

ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/api/texto-ejemplo', methods=['GET'])
def obtener_texto_ejemplo():
    """Endpoint para obtener un texto aleatorio para el ejercicio de lectura"""
    texto = random.choice(TEXTOS_EJEMPLO)
    return jsonify({
        'texto': texto,
        'instrucciones': 'Por favor, lea el siguiente texto en voz alta y clara:'
    })

@bp.route('/api/audio/procesar', methods=['POST'])
def procesar_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No se encontró el archivo de audio'}), 400
    
    audio_file = request.files['audio']
    if audio_file.filename == '':
        return jsonify({'error': 'No se seleccionó ningún archivo'}), 400
    
    if not allowed_file(audio_file.filename):
        return jsonify({'error': 'Tipo de archivo no permitido'}), 400

    try:
        # Guardar el archivo temporalmente
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            audio_file.save(temp_file.name)
            
            # Cargar el audio con soundfile para análisis
            data, sample_rate = sf.read(temp_file.name)
            
            # Análisis de audio
            duration = len(data) / sample_rate
            intensity = np.abs(data).mean()
            
            # Transcripción con speech_recognition
            recognizer = sr.Recognizer()
            with sr.AudioFile(temp_file.name) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data, language='es-ES')
            
            # Calcular métricas
            words = len(text.split())
            wpm = (words / duration) * 60
            
            # Limpiar archivo temporal
            os.unlink(temp_file.name)
            
            return jsonify({
                'texto': text,
                'duracion': duration,
                'palabras_por_minuto': wpm,
                'intensidad': float(intensity),
                'palabras_totales': words
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'}) 