from flask import Blueprint, request, jsonify, send_file
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
from difflib import SequenceMatcher
import re
from gtts import gTTS

rutas = Blueprint('rutas', __name__)

# Configuración de rutas para archivos temporales
TEMP_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp')
if not os.path.exists(TEMP_FOLDER):
    os.makedirs(TEMP_FOLDER)

# Textos organizados por nivel de dificultad
TEXTOS_POR_NIVEL = {
    'principiante': [
    "El sol brillaba intensamente sobre las montañas nevadas, mientras las águilas volaban majestuosamente en círculos sobre el valle verde y frondoso.",
    "En el mercado local, los vendedores pregonaban sus productos frescos, creando una sinfonía de voces y aromas que llenaban el aire.",
        "La biblioteca estaba en silencio, solo se escuchaba el suave pasar de las páginas y el ocasional suspiro de algún estudiante concentrado."
    ],
    'intermedio': [
        "La extraordinaria biodiversidad del ecosistema amazónico está siendo amenazada por la deforestación descontrolada y el cambio climático global, provocando preocupación entre los científicos y ambientalistas.",
        "Durante la presentación multimedia, el conferencista explicó detalladamente cómo la inteligencia artificial transformará significativamente nuestra forma de trabajar y relacionarnos en el próximo quinquenio.",
        "Los arqueólogos descubrieron jeroglíficos prehistóricos que describían minuciosamente las constelaciones y los fenómenos astronómicos observados por antiguas civilizaciones mesoamericanas."
    ],
    'avanzado': [
        "La interdisciplinariedad característica de la neuropsicología contemporánea ha permitido establecer correlaciones significativas entre la plasticidad sináptica y el desarrollo de habilidades cognitivas específicas, particularmente en el aprendizaje de idiomas.",
        "Los paradigmas socioeconómicos tradicionales están siendo cuestionados por la implementación exponencial de tecnologías descentralizadas, como las criptomonedas y los contratos inteligentes, que revolucionan las transacciones financieras globales.",
        "La espectrofotometría de absorción atómica, complementada con técnicas cromatográficas avanzadas, permite identificar concentraciones extraordinariamente pequeñas de elementos químicos en muestras medioambientales complejas."
    ]
}

# Textos para dictado por nivel
DICTADOS_POR_NIVEL = {
    'principiante': [
        "El cielo estaba despejado y el sol brillaba con intensidad sobre la ciudad.",
        "Los niños jugaban alegremente en el parque mientras sus padres conversaban.",
        "La música del piano llenaba la habitación con dulces melodías."
    ],
    'intermedio': [
        "La investigación científica ha demostrado que el ejercicio regular mejora significativamente la capacidad cognitiva y el bienestar emocional.",
        "Los avances tecnológicos en energías renovables están transformando nuestra manera de generar y consumir electricidad.",
        "La preservación de los ecosistemas naturales es fundamental para mantener el equilibrio medioambiental."
    ],
    'avanzado': [
        "La implementación de metodologías pedagógicas innovadoras ha revolucionado la manera en que se abordan las dificultades de aprendizaje en contextos educativos contemporáneos.",
        "La interconectividad global y el desarrollo de tecnologías emergentes están redefiniendo los paradigmas socioeconómicos tradicionales.",
        "La biodiversidad de los ecosistemas tropicales está siendo amenazada por múltiples factores antropogénicos y cambios climáticos significativos."
    ]
}

ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg', 'webm'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@rutas.route('/api/v1/ejercicios/lectura', methods=['GET'])
def obtener_texto_lectura():
    """Endpoint para obtener un texto aleatorio para el ejercicio de lectura"""
    texto = random.choice(TEXTOS_POR_NIVEL['principiante'])
    return jsonify({
        'texto': texto
    })

@rutas.route('/api/v1/ejercicios/dictado', methods=['GET'])
def obtener_audio_dictado():
    """Endpoint para obtener el audio para el ejercicio de dictado"""
    try:
        # Seleccionar un texto aleatorio para el dictado
        texto = random.choice(DICTADOS_POR_NIVEL['principiante'])
        
        # Crear el archivo de audio usando gTTS
        tts = gTTS(text=texto, lang='es')
        
        # Guardar el audio temporalmente
        temp_audio_path = os.path.join(TEMP_FOLDER, 'dictado_temp.mp3')
        tts.save(temp_audio_path)
        
        # Enviar el archivo de audio
        return send_file(
            temp_audio_path,
            mimetype='audio/mp3',
            as_attachment=True,
            download_name='dictado.mp3'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@rutas.route('/api/v1/ejercicios/dictado/evaluar', methods=['POST'])
def evaluar_dictado():
    """Endpoint para evaluar la respuesta del ejercicio de dictado"""
    try:
        data = request.get_json()
        texto_usuario = data.get('texto_usuario', '').strip()
        
        if not texto_usuario:
            return jsonify({'error': 'No se proporcionó texto'}), 400
        
        # Por ahora, comparamos con un texto fijo (esto deberá mejorarse)
        texto_original = DICTADOS_POR_NIVEL['principiante'][0]
        
        # Calcular similitud
        similitud = calcular_similitud_texto(texto_original, texto_usuario)
        
        # Analizar errores
        errores = analizar_errores_dislexia(texto_original, texto_usuario)
        
        # Calcular puntuación (0-100)
        puntuacion = similitud * 100
        
        return jsonify({
            'puntuacion_general': round(puntuacion, 1),
            'precision': round(similitud * 100, 1),
            'fluidez': 85.0,  # Valor ejemplo
            'comprension': 90.0,  # Valor ejemplo
            'detalles_analisis': [
                {
                    'descripcion': 'Precisión en la escritura',
                    'cumplido': similitud > 0.8
                },
                {
                    'descripcion': 'Uso correcto de signos de puntuación',
                    'cumplido': True  # Ejemplo
                }
            ],
            'recomendaciones': [
                'Practique la escritura de palabras complejas',
                'Revise el uso de mayúsculas y puntuación'
            ]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@rutas.route('/api/v1/ejercicios/lectura/evaluar', methods=['POST'])
def evaluar_lectura():
    """Endpoint para evaluar el ejercicio de lectura"""
    if 'audio' not in request.files:
        return jsonify({'error': 'No se encontró el archivo de audio'}), 400
    
    audio_file = request.files['audio']
    texto = request.form.get('texto')
    
    if audio_file.filename == '':
        return jsonify({'error': 'No se seleccionó ningún archivo'}), 400
    
    if not texto:
        return jsonify({'error': 'No se proporcionó el texto'}), 400
    
    try:
        # Guardar el archivo temporal
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        audio_file.save(temp_file.name)
        
        # Procesar el audio (aquí iría la lógica real de procesamiento)
        # Por ahora devolvemos datos de ejemplo
        return jsonify({
            'puntuacion_general': 85.5,
            'precision': 88.0,
            'fluidez': 82.0,
            'comprension': 86.0,
            'detalles_analisis': [
                {
                    'descripcion': 'Pronunciación clara',
                    'cumplido': True
                },
                {
                    'descripcion': 'Velocidad de lectura adecuada',
                    'cumplido': True
                }
            ],
            'recomendaciones': [
                'Practique la pronunciación de palabras largas',
                'Mantenga un ritmo constante durante la lectura'
            ]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Limpiar archivos temporales
        if 'temp_file' in locals():
            os.unlink(temp_file.name)

def calcular_similitud_texto(texto_original, texto_transcrito):
    """Calcula la similitud entre el texto original y el transcrito"""
    return SequenceMatcher(None, texto_original.lower(), texto_transcrito.lower()).ratio()

def calcular_similitud_palabras(palabra1, palabra2):
    """Calcula la similitud entre dos palabras usando distancia de Levenshtein"""
    if len(palabra1) == 0 or len(palabra2) == 0:
        return 0
    
    matriz = [[0] * (len(palabra2) + 1) for _ in range(len(palabra1) + 1)]
    
    for i in range(len(palabra1) + 1):
        matriz[i][0] = i
    for j in range(len(palabra2) + 1):
        matriz[0][j] = j
        
    for i in range(1, len(palabra1) + 1):
        for j in range(1, len(palabra2) + 1):
            if palabra1[i-1] == palabra2[j-1]:
                matriz[i][j] = matriz[i-1][j-1]
            else:
                matriz[i][j] = min(
                    matriz[i-1][j] + 1,    # eliminación
                    matriz[i][j-1] + 1,    # inserción
                    matriz[i-1][j-1] + 1   # sustitución
                )
    
    distancia = matriz[len(palabra1)][len(palabra2)]
    max_len = max(len(palabra1), len(palabra2))
    return 1 - (distancia / max_len)

def analizar_errores_dislexia(texto_original, texto_transcrito):
    """Analiza errores comunes asociados con dislexia"""
    # Normalizar textos: eliminar espacios extra y convertir a minúsculas
    texto_original = ' '.join(texto_original.lower().split())
    texto_transcrito = ' '.join(texto_transcrito.lower().split())
    
    errores = {
        'inversiones': 0,
        'omisiones': 0,
        'adiciones': 0,
        'sustituciones': 0
    }
    
    # Dividir en palabras y limpiar signos de puntuación
    def limpiar_palabra(palabra):
        return ''.join(c for c in palabra.lower() if c.isalnum())
    
    palabras_original = [limpiar_palabra(p) for p in texto_original.split()]
    palabras_transcrito = [limpiar_palabra(p) for p in texto_transcrito.split()]
    
    # Analizar cada palabra del texto transcrito
    for i, palabra_trans in enumerate(palabras_transcrito):
        if i >= len(palabras_original):
            errores['adiciones'] += 1
            continue
            
        palabra_orig = palabras_original[i]
        
        if palabra_trans == palabra_orig:
            continue
            
        # Verificar inversiones (mismo conjunto de letras, diferente orden)
        if sorted(palabra_trans) == sorted(palabra_orig) and palabra_trans != palabra_orig:
            errores['inversiones'] += 1
            continue
            
        # Calcular similitud entre palabras
        similitud = calcular_similitud_palabras(palabra_orig, palabra_trans)
        
        # Verificar omisiones
        if len(palabra_trans) < len(palabra_orig):
            if palabra_trans in palabra_orig or similitud > 0.7:
                errores['omisiones'] += 1
                continue
        
        # Verificar adiciones
        if len(palabra_trans) > len(palabra_orig):
            if palabra_orig in palabra_trans or similitud > 0.7:
                errores['adiciones'] += 1
                continue
        
        # Verificar sustituciones (palabras diferentes pero similares)
        if similitud < 0.8:  # Si las palabras son suficientemente diferentes
            errores['sustituciones'] += 1
    
    # Ajustar omisiones si hay palabras faltantes al final
    if len(palabras_transcrito) < len(palabras_original):
        errores['omisiones'] += len(palabras_original) - len(palabras_transcrito)
    
    return errores

def determinar_siguiente_nivel(nivel_actual, puntuacion, errores):
    """Determina el siguiente nivel basado en el desempeño"""
    niveles = ['principiante', 'intermedio', 'avanzado']
    indice_actual = niveles.index(nivel_actual)
    
    # Criterios para avanzar:
    # - Puntuación > 85%
    # - Pocos errores totales (menos de 3)
    if puntuacion > 85 and sum(errores.values()) < 3 and indice_actual < len(niveles) - 1:
        return niveles[indice_actual + 1]
    
    # Criterios para retroceder:
    # - Puntuación < 60%
    # - Muchos errores (más de 5)
    if (puntuacion < 60 or sum(errores.values()) > 5) and indice_actual > 0:
        return niveles[indice_actual - 1]
    
    return nivel_actual

@rutas.route('/api/audio/procesar', methods=['POST'])
def procesar_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No se encontró el archivo de audio'}), 400
    
    audio_file = request.files['audio']
    texto_original = request.form.get('texto_original')
    nivel_actual = request.form.get('nivel_actual', 'principiante')
    
    if audio_file.filename == '':
        return jsonify({'error': 'No se seleccionó ningún archivo'}), 400
    
    if not texto_original:
        return jsonify({'error': 'No se proporcionó el texto original'}), 400
    
    if not allowed_file(audio_file.filename):
        return jsonify({'error': f'Tipo de archivo no permitido. Formatos permitidos: {", ".join(ALLOWED_EXTENSIONS)}'}), 400

    temp_file = None
    wav_path = None
    try:
        # Guardar el archivo temporal con extensión webm
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.webm')
            audio_file.save(temp_file.name)
        temp_file.close()  # Cerrar el archivo temporal
        
        # Convertir webm a wav usando pydub
        audio = AudioSegment.from_file(temp_file.name)
        wav_path = temp_file.name.replace('.webm', '.wav')
        audio.export(wav_path, format='wav')
        
        # Procesar el archivo wav
        data, sample_rate = sf.read(wav_path)
            duration = len(data) / sample_rate
            intensity = np.abs(data).mean()
            
            recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
                audio_data = recognizer.record(source)
            texto_transcrito = recognizer.recognize_google(audio_data, language='es-ES')
            
        # Análisis de patrones
        similitud = calcular_similitud_texto(texto_original, texto_transcrito)
        errores = analizar_errores_dislexia(texto_original, texto_transcrito)
        palabras = len(texto_transcrito.split())
        wpm = (palabras / duration) * 60
            
        # Calcular puntuación general (0-100)
        total_errores = sum(errores.values())
        palabras_totales = len(texto_original.split())
        ratio_errores = total_errores / palabras_totales if palabras_totales > 0 else 1
        
        puntuacion = (
            (similitud * 40) +  # Precisión de lectura: 40%
            (min(wpm/150, 1) * 30) +  # Velocidad de lectura: 30%
            (max(0, 1 - ratio_errores) * 30)  # Errores: 30%
        )

        # Determinar el siguiente nivel
        siguiente_nivel = determinar_siguiente_nivel(nivel_actual, puntuacion, errores)
        
        # Seleccionar el siguiente texto basado en el nuevo nivel
        siguiente_texto = random.choice(TEXTOS_POR_NIVEL[siguiente_nivel])
    
    return jsonify({
            'texto_original': texto_original,
            'texto_transcrito': texto_transcrito,
                'duracion': duration,
                'palabras_por_minuto': wpm,
            'palabras_totales': palabras,
            'precision_lectura': similitud * 100,
            'errores_detectados': errores,
            'puntuacion_general': min(max(puntuacion, 0), 100),
            'intensidad_voz': float(intensity),
            'siguiente_nivel': siguiente_nivel,
            'siguiente_texto': siguiente_texto,
            'recomendaciones': [
                "Practica la lectura en voz alta diariamente" if wpm < 100 else None,
                "Enfócate en la precisión de la lectura" if similitud < 0.8 else None,
                "Presta atención a las inversiones de letras" if errores['inversiones'] > 0 else None,
                "Cuida no omitir letras al leer" if errores['omisiones'] > 2 else None,
                "Intenta mantener un ritmo constante de lectura" if errores['adiciones'] > 2 else None
            ]
            })
            
    except Exception as e:
        print(f"Error al procesar el audio: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        # Limpiar archivos temporales
        try:
            if temp_file and os.path.exists(temp_file.name):
                os.close(temp_file.fileno())  # Cerrar el descriptor de archivo
                os.unlink(temp_file.name)
            if wav_path and os.path.exists(wav_path):
                os.unlink(wav_path)
        except Exception as e:
            print(f"Error al eliminar archivos temporales: {str(e)}")
            pass

@rutas.route('/api/health', methods=['GET'])
def health_check():
    """Endpoint para verificar el estado del servicio"""
    return jsonify({'estado': 'ok'})

@rutas.route('/api/dictado/obtener', methods=['GET'])
def obtener_dictado():
    """Endpoint para obtener un ejercicio de dictado"""
    nivel = request.args.get('nivel', 'principiante')
    if nivel not in DICTADOS_POR_NIVEL:
        nivel = 'principiante'
    
    texto = random.choice(DICTADOS_POR_NIVEL[nivel])
    
    # Generar audio del texto
    try:
        tts = gTTS(text=texto, lang='es')
        audio_path = os.path.join(TEMP_FOLDER, f'dictado_{hash(texto)}.mp3')
        tts.save(audio_path)
        
        return jsonify({
            'texto': texto,
            'audio_url': f'/audio/dictado_{hash(texto)}.mp3',
            'nivel': nivel
        })
    except Exception as e:
        print(f"Error al generar audio: {str(e)}")
        return jsonify({'error': 'Error al generar el audio'}), 500

@rutas.route('/api/dictado/verificar', methods=['POST'])
def verificar_dictado():
    """Endpoint para verificar un ejercicio de dictado"""
    data = request.get_json()
    if not data or 'texto_usuario' not in data or 'texto_original' not in data:
        return jsonify({'error': 'Datos incompletos'}), 400
    
    texto_usuario = data['texto_usuario']
    texto_original = data['texto_original']
    nivel_actual = data.get('nivel_actual', 'principiante')
    
    # Analizar errores
    similitud = calcular_similitud_texto(texto_original, texto_usuario)
    errores = analizar_errores_dislexia(texto_original, texto_usuario)
    
    # Calcular puntuación
    total_errores = sum(errores.values())
    palabras_totales = len(texto_original.split())
    ratio_errores = total_errores / palabras_totales if palabras_totales > 0 else 1
    
    puntuacion = (
        (similitud * 60) +  # Precisión: 60%
        (max(0, 1 - ratio_errores) * 40)  # Errores: 40%
    )
    
    # Determinar siguiente nivel
    siguiente_nivel = determinar_siguiente_nivel(nivel_actual, puntuacion, errores)
    
    return jsonify({
        'puntuacion': min(max(puntuacion, 0), 100),
        'errores': errores,
        'siguiente_nivel': siguiente_nivel,
        'recomendaciones': [
            "Practica la escritura de palabras similares" if errores['sustituciones'] > 2 else None,
            "Presta atención a los signos de puntuación" if similitud < 0.8 else None,
            "Revisa cuidadosamente lo que escribes" if total_errores > 5 else None
        ]
    }) 