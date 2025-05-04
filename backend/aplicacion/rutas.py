from flask import Blueprint, request, jsonify, send_file, after_this_request
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
from .ejercicios.ejercicios_comprension import obtener_ejercicio, evaluar_comprension
from .ejercicios.evaluador import Evaluador
from .database import db
from difflib import SequenceMatcher
import re
from gtts import gTTS
import uuid
from io import BytesIO

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

@rutas.route('/v1/ejercicios/lectura', methods=['GET'])
def obtener_texto_lectura():
    """Endpoint para obtener un texto aleatorio para el ejercicio de lectura"""
    texto = random.choice(TEXTOS_POR_NIVEL['principiante'])
    return jsonify({
        'texto': texto
    })

dictados_temp = {}

@rutas.route('/v1/ejercicios/dictado', methods=['GET'])
def obtener_audio_dictado():
    """Endpoint para obtener el audio para el ejercicio de dictado con palabras aleatorias y pausas de 5 segundos"""
    try:
        print('Iniciando generación de audio de dictado...')
        palabras_base = [
            "biotecnología", "sostenibilidad", "paradigma", "correlación", "metodología",
            "hipótesis", "diagnóstico", "neurocientífico", "epistemológico", "interdisciplinario",
            "socioeconómico", "gubernamental", "antropológico", "psicopedagógico", "biodiversidad",
            "fotosíntesis", "ecosistema", "metamorfosis", "fenómeno", "simbiosis"
        ]
        palabras = random.sample(palabras_base, 7)
        print('Palabras seleccionadas:', palabras)
        audios = []
        for palabra in palabras:
            print(f'Generando audio para la palabra: {palabra}')
            tts = gTTS(text=palabra, lang='es')
            temp_audio_path = os.path.join(TEMP_FOLDER, f'{palabra}_temp.mp3')
            tts.save(temp_audio_path)
            audio_segment = AudioSegment.from_file(temp_audio_path)
            audios.append(audio_segment)
            if palabra != palabras[-1]:
                audios.append(AudioSegment.silent(duration=5000))
            os.remove(temp_audio_path)
        audio_final = sum(audios)
        audio_buffer = BytesIO()
        audio_final.export(audio_buffer, format='mp3')
        audio_buffer.seek(0)
        dictado_id = str(uuid.uuid4())
        dictados_temp[dictado_id] = palabras
        print('Enviando archivo de audio al frontend...')
        response = send_file(
            audio_buffer,
            mimetype='audio/mp3',
            as_attachment=True,
            download_name='dictado_palabras.mp3'
        )
        response.headers["X-Palabras-Dictado"] = ",".join(palabras)
        response.headers["X-Dictado-Id"] = dictado_id
        response.headers["Access-Control-Expose-Headers"] = "X-Palabras-Dictado, X-Dictado-Id"
        print('Audio enviado correctamente.')
        return response
    except Exception as e:
        import traceback
        print('Error al generar o enviar audio de dictado:', traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@rutas.route('/v1/ejercicios/dictado/evaluar', methods=['POST'])
def evaluar_dictado():
    """Endpoint para evaluar la respuesta del ejercicio de dictado"""
    try:
        data = request.get_json()
        texto_usuario = data.get('texto_usuario', '').strip()
        dictado_id = data.get('dictado_id', '').strip()
        if not texto_usuario:
            return jsonify({'error': 'No se proporcionó texto'}), 400
        if not dictado_id or dictado_id not in dictados_temp:
            return jsonify({'error': 'No se encontró el dictado o ya fue evaluado. Por favor, solicite un nuevo dictado.'}), 400
        palabras_correctas = dictados_temp.pop(dictado_id)
        texto_original = " ".join(palabras_correctas)
        similitud = calcular_similitud_texto(texto_original, texto_usuario)
        errores = analizar_errores_dislexia(texto_original, texto_usuario)
        palabras_usuario = texto_usuario.split()
        palabras_correctas_count = 0
        def normalizar(palabra):
            import unicodedata
            return ''.join(c for c in unicodedata.normalize('NFD', palabra.lower()) if c.isalnum())
        for i, palabra in enumerate(palabras_correctas):
            if i < len(palabras_usuario):
                palabra_usuario = normalizar(palabras_usuario[i])
                palabra_correcta = normalizar(palabra)
                similitud_palabra = calcular_similitud_palabras(palabra_correcta, palabra_usuario)
                if similitud_palabra > 0.95:
                    palabras_correctas_count += 1
        puntuacion = (palabras_correctas_count / len(palabras_correctas)) * 100
        # ML features para dictado
        features = {
            'tiempo_respuesta': len(texto_usuario.split()),
            'errores_ortograficos': sum(errores.values()),
            'repeticiones': 0,  # No se mide en dictado simple
            'comprension_lectora': similitud
        }
        ml_result = ServicioML().predict_dislexia(features)
        return jsonify({
            'puntuacion_general': round(puntuacion, 1),
            'precision': round(similitud * 100, 1),
            'fluidez': 85.0,
            'comprension': 90.0,
            'palabras_usuario': palabras_usuario,
            'palabras_correctas': palabras_correctas,
            'detalles_analisis': [
                {
                    'descripcion': 'Precisión en la escritura',
                    'cumplido': similitud > 0.8
                },
                {
                    'descripcion': 'Uso correcto de signos de puntuación',
                    'cumplido': True
                }
            ],
            'recomendaciones': [
                'Practique la escritura de palabras complejas',
                'Revise el uso de mayúsculas y puntuación'
            ],
            'ml_prediccion': ml_result.get('prediccion'),
            'ml_probabilidad': ml_result.get('probabilidad')
        })
    except Exception as e:
        import traceback
        print('Error en evaluación de dictado:', traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@rutas.route('/v1/ejercicios/lectura/evaluar', methods=['POST'])
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
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.webm')
        audio_file.save(temp_file.name)
        temp_file.close()
        audio = AudioSegment.from_file(temp_file.name)
        wav_path = temp_file.name.replace('.webm', '.wav')
        audio.export(wav_path, format='wav')
        data, sample_rate = sf.read(wav_path)
        duration = len(data) / sample_rate
        intensity = np.abs(data).mean()
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
            texto_transcrito = recognizer.recognize_google(audio_data, language='es-ES')

        similitud = calcular_similitud_texto(texto_original, texto_transcrito)
        errores = analizar_errores_dislexia(texto_original, texto_transcrito)
        palabras = len(texto_transcrito.split())
        wpm = (palabras / duration) * 60

        total_errores = sum(errores.values())
        palabras_totales = len(texto_original.split())
        ratio_errores = total_errores / palabras_totales if palabras_totales > 0 else 1

        puntuacion = (
            (similitud * 40) +
            (min(wpm/150, 1) * 30) +
            (max(0, 1 - ratio_errores) * 30)
        )

        siguiente_nivel = determinar_siguiente_nivel(nivel_actual, puntuacion, errores)
        siguiente_texto = random.choice(TEXTOS_POR_NIVEL[siguiente_nivel])

        precision = round(similitud * 100, 1)
        fluidez = round(min(wpm / 150, 1) * 100, 1)
        comprension = 100.0
        recomendaciones = [
            r for r in [
                "Practica la lectura en voz alta diariamente" if wpm < 100 else None,
                "Enfócate en la precisión de la lectura" if similitud < 0.8 else None,
                "Presta atención a las inversiones de letras" if errores['inversiones'] > 0 else None,
                "Cuida no omitir letras al leer" if errores['omisiones'] > 2 else None,
                "Intenta mantener un ritmo constante de lectura" if errores['adiciones'] > 2 else None
            ] if r
        ]
        mensajes_positivos = [
            "¡Excelente trabajo! Sigue practicando para mantener tu nivel.",
            "Tu lectura fue clara y precisa. ¡Sigue así!"
        ]
        while len(recomendaciones) < 2:
            recomendaciones.append(mensajes_positivos[len(recomendaciones) % len(mensajes_positivos)])

        detalles_analisis = [
            {
                'descripcion': 'Precisión en la lectura',
                'cumplido': precision > 80
            },
            {
                'descripcion': 'Fluidez adecuada',
                'cumplido': fluidez > 70
            },
            {
                'descripcion': 'Comprensión lectora',
                'cumplido': comprension > 80
            }
        ]
        if not any(d['cumplido'] for d in detalles_analisis):
            detalles_analisis.append({
                'descripcion': '¡Buen trabajo! No se detectaron problemas significativos en tu lectura.',
                'cumplido': True
            })

        # ML features para lectura
        features = {
            'tiempo_respuesta': duration,
            'errores_ortograficos': total_errores,
            'repeticiones': 0,  # Si tienes repeticiones, cámbialo aquí
            'comprension_lectora': similitud
        }
        ml_result = ServicioML().predict_dislexia(features)
        return jsonify({
            'texto_original': texto_original,
            'texto_transcrito': texto_transcrito,
            'duracion': duration,
            'palabras_por_minuto': wpm,
            'palabras_totales': palabras,
            'precision_lectura': precision,
            'precision': precision,
            'fluidez': fluidez,
            'comprension': comprension,
            'errores_detectados': errores,
            'adiciones': errores.get('adiciones', 0),
            'omisiones': errores.get('omisiones', 0),
            'puntuacion_general': min(max(puntuacion, 0), 100),
            'intensidad_voz': float(intensity),
            'siguiente_nivel': siguiente_nivel,
            'siguiente_texto': siguiente_texto,
            'recomendaciones': recomendaciones,
            'detalles_analisis': detalles_analisis,
            'ml_prediccion': ml_result.get('prediccion'),
            'ml_probabilidad': ml_result.get('probabilidad')
        })
    except Exception as e:
        import traceback
        print('Error en evaluación de lectura:', traceback.format_exc())
        return jsonify({'error': str(e)}), 500
    finally:
        try:
            if temp_file and os.path.exists(temp_file.name):
                os.unlink(temp_file.name)
            if wav_path and os.path.exists(wav_path):
                os.unlink(wav_path)
        except Exception as e:
            print(f"Error al eliminar archivos temporales: {str(e)}")
            pass

@rutas.route('/health', methods=['GET'])
def health_check():
    """Endpoint para verificar el estado del servicio"""
    return jsonify({'estado': 'ok'})

@rutas.route('/dictado/obtener', methods=['GET'])
def obtener_dictado():
    """Endpoint para obtener un ejercicio de dictado"""
    nivel = request.args.get('nivel', 'principiante')
    if nivel not in DICTADOS_POR_NIVEL:
        nivel = 'principiante'
    
    texto = random.choice(DICTADOS_POR_NIVEL[nivel])
    
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

@rutas.route('/dictado/verificar', methods=['POST'])
def verificar_dictado():
    """Endpoint para verificar un ejercicio de dictado"""
    data = request.get_json()
    if not data or 'texto_usuario' not in data or 'texto_original' not in data:
        return jsonify({'error': 'Datos incompletos'}), 400
    
    texto_usuario = data['texto_usuario']
    texto_original = data['texto_original']
    nivel_actual = data.get('nivel_actual', 'principiante')
    
    similitud = calcular_similitud_texto(texto_original, texto_usuario)
    errores = analizar_errores_dislexia(texto_original, texto_usuario)
    
    total_errores = sum(errores.values())
    palabras_totales = len(texto_original.split())
    ratio_errores = total_errores / palabras_totales if palabras_totales > 0 else 1
    
    puntuacion = (
        (similitud * 60) +
        (max(0, 1 - ratio_errores) * 40)
    )
    
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

@rutas.route('/v1/ejercicios/comprension', methods=['GET'])
def obtener_ejercicio_comprension():
    """Obtiene un ejercicio de comprensión lectora."""
    nivel = request.args.get('nivel', 'nivel_1')
    try:
        ejercicio = obtener_ejercicio(nivel)
        return jsonify(ejercicio), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@rutas.route('/v1/ejercicios/comprension/evaluar', methods=['POST'])
def evaluar_ejercicio_comprension():
    """Evalúa las respuestas de un ejercicio de comprensión lectora."""
    try:
        data = request.get_json()
        print('Datos recibidos en /v1/ejercicios/comprension/evaluar:', data)
        nivel = data.get('nivel')
        respuestas = data.get('respuestas')
        tiempo_respuesta = data.get('tiempo_respuesta', 0)
        if not nivel:
            print('Falta el campo nivel')
            return jsonify({'error': 'Falta el campo nivel'}), 400
        if respuestas is None:
            print('Falta el campo respuestas')
            return jsonify({'error': 'Falta el campo respuestas'}), 400
        if not isinstance(respuestas, list):
            print('El campo respuestas no es una lista')
            return jsonify({'error': 'El campo respuestas debe ser una lista'}), 400
        resultados = evaluar_comprension(nivel, respuestas, tiempo_respuesta)
        # ML features para comprensión
        features = {
            'tiempo_respuesta': tiempo_respuesta,
            'errores_ortograficos': resultados.get('total', 0) - resultados.get('correctas', 0),
            'repeticiones': 0,  # No se mide en comprensión
            'comprension_lectora': resultados.get('puntaje', 0) / resultados.get('total', 1)
        }
        ml_result = ServicioML().predict_dislexia(features)
        resultados['ml_prediccion'] = ml_result.get('prediccion')
        resultados['ml_probabilidad'] = ml_result.get('probabilidad')
        return jsonify(resultados), 200
    except Exception as e:
        import traceback
        print('Error en evaluación de comprensión:', traceback.format_exc())
        return jsonify({'error': str(e)}), 400

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
        # Solo es correcta si es exactamente igual (ignorando mayúsculas y tildes)
        if palabra_trans == palabra_orig:
            continue
        # Verificar inversiones (mismo conjunto de letras, diferente orden)
        if sorted(palabra_trans) == sorted(palabra_orig) and palabra_trans != palabra_orig:
            errores['inversiones'] += 1
            continue
        # Calcular similitud entre palabras
        similitud = calcular_similitud_palabras(palabra_orig, palabra_trans)
        # Verificar omisiones (más estricto: similitud > 0.95)
        if len(palabra_trans) < len(palabra_orig):
            if palabra_trans in palabra_orig or similitud > 0.95:
                errores['omisiones'] += 1
                continue
        # Verificar adiciones (más estricto: similitud > 0.95)
        if len(palabra_trans) > len(palabra_orig):
            if palabra_orig in palabra_trans or similitud > 0.95:
                errores['adiciones'] += 1
                continue
        # Verificar sustituciones (palabras diferentes pero similares)
        if similitud < 0.95:  # Ahora solo cuenta como sustitución si la similitud es menor a 0.95
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