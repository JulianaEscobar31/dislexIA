from flask import Blueprint, request, jsonify
from app.services.exercise_service import exercise_service
from app.services.audio_service import audio_service
from app.services.ml_service import ml_service
from app.database.models import Evaluacion
from app import db
from datetime import datetime
from app.services.utils import validar_datos_evaluacion, manejar_errores

api = Blueprint('api', __name__)

@api.route('/ejercicios/<tipo>', methods=['GET'])
def obtener_ejercicio(tipo):
    """Obtiene un nuevo ejercicio del tipo especificado"""
    try:
        ejercicio = exercise_service.generar_ejercicio(tipo)
        if 'error' in ejercicio:
            return jsonify(ejercicio), 400
        return jsonify(ejercicio)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route('/ejercicios/<tipo>/evaluar', methods=['POST'])
def evaluar_ejercicio(tipo):
    """Evalúa un ejercicio completado"""
    try:
        datos = request.get_json()
        if not datos:
            return jsonify({"error": "No se proporcionaron datos"}), 400

        # Validar datos requeridos según el tipo de ejercicio
        campos_requeridos = {
            'lectura': ['texto', 'tiempo_respuesta', 'errores', 'repeticiones'],
            'dictado': ['texto', 'tiempo_respuesta', 'errores_ortograficos'],
            'comprension': ['respuestas', 'tiempo_respuesta', 'comprension_lectora']
        }

        if tipo not in campos_requeridos:
            return jsonify({"error": "Tipo de ejercicio no válido"}), 400

        for campo in campos_requeridos[tipo]:
            if campo not in datos:
                return jsonify({"error": f"Falta el campo requerido: {campo}"}), 400

        # Procesar la evaluación según el tipo
        resultado = ml_service.evaluar_ejercicio(tipo, datos)
        
        # Crear registro de evaluación
        evaluacion = Evaluacion(
            fecha_evaluacion=datetime.utcnow(),
            tiempo_respuesta=datos.get('tiempo_respuesta', 0),
            errores_ortograficos=datos.get('errores_ortograficos', 0),
            repeticiones=datos.get('repeticiones', 0),
            comprension_lectora=datos.get('comprension_lectora', 0),
            prediccion=resultado['prediccion'],
            confianza_prediccion=resultado['confianza']
        )

        # Guardar el ejercicio específico
        if tipo == 'lectura':
            evaluacion.ejercicio_lectura = datos
        elif tipo == 'dictado':
            evaluacion.ejercicio_dictado = datos
        elif tipo == 'comprension':
            evaluacion.ejercicio_comprension = datos

        db.session.add(evaluacion)
        db.session.commit()

        return jsonify({
            "mensaje": "Evaluación completada con éxito",
            "resultado": resultado,
            "evaluacion_id": evaluacion.id
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@api.route('/audio/procesar', methods=['POST'])
def procesar_audio():
    """Procesa un archivo de audio de lectura"""
    try:
        if 'audio' not in request.files:
            return jsonify({"error": "No se recibió archivo de audio"}), 400
            
        audio_file = request.files['audio']
        if not audio_file.filename:
            return jsonify({"error": "Nombre de archivo vacío"}), 400
            
        # Guardar archivo temporalmente
        temp_path = f"temp_{audio_file.filename}"
        audio_file.save(temp_path)
        
        try:
            # Procesar audio
            resultados = audio_service.procesar_audio(temp_path)
            
            # Analizar con ML si hay suficientes datos
            if resultados.get("texto_transcrito"):
                prediccion = ml_service.predict_dislexia({
                    "tiempo_respuesta": resultados["metricas"]["duracion"],
                    "errores_ortograficos": 0,  # Se podría implementar detección de errores
                    "repeticiones": resultados["metricas"]["numero_pausas"],
                    "comprension_lectora": resultados["metricas"]["fluidez"]
                })
                resultados["prediccion"] = prediccion
            
            return jsonify(resultados)
        finally:
            # Limpiar archivo temporal
            import os
            if os.path.exists(temp_path):
                os.remove(temp_path)
                
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route('/evaluaciones', methods=['POST'])
@manejar_errores
def crear_evaluacion():
    data = request.get_json()
    
    errores = validar_datos_evaluacion(data)
    if errores:
        return jsonify({'errores': errores}), 400
    
    nueva_evaluacion = Evaluacion(
        tiempo_respuesta=data['tiempo_respuesta'],
        errores_ortograficos=data['errores_ortograficos'],
        repeticiones=data['repeticiones'],
        comprension_lectora=data['comprension_lectora'],
        ejercicio_dictado=data['ejercicio_dictado'],
        ejercicio_lectura=data['ejercicio_lectura'],
        ejercicio_comprension=data['ejercicio_comprension'],
        prediccion=data['prediccion'],
        confianza_prediccion=data['confianza_prediccion']
    )
    
    db.session.add(nueva_evaluacion)
    db.session.commit()
    
    return jsonify({
        'mensaje': 'Evaluación creada exitosamente',
        'id': nueva_evaluacion.id
    }), 201

@api.route('/evaluaciones', methods=['GET'])
@manejar_errores
def obtener_evaluaciones():
    evaluaciones = Evaluacion.query.all()
    return jsonify([evaluacion.to_dict() for evaluacion in evaluaciones]), 200

@api.route('/evaluaciones/<int:id>', methods=['GET'])
@manejar_errores
def obtener_evaluacion(id):
    evaluacion = Evaluacion.query.get_or_404(id)
    return jsonify(evaluacion.to_dict()), 200

@api.route('/evaluaciones/<int:id>', methods=['DELETE'])
@manejar_errores
def eliminar_evaluacion(id):
    evaluacion = Evaluacion.query.get_or_404(id)
    db.session.delete(evaluacion)
    db.session.commit()
    return jsonify({'mensaje': 'Evaluación eliminada exitosamente'}), 200

@api.route('/estadisticas', methods=['GET'])
@manejar_errores
def obtener_estadisticas():
    total_evaluaciones = Evaluacion.query.count()
    evaluaciones_positivas = Evaluacion.query.filter_by(prediccion=True).count()
    evaluaciones_negativas = Evaluacion.query.filter_by(prediccion=False).count()
    
    return jsonify({
        'total_evaluaciones': total_evaluaciones,
        'evaluaciones_positivas': evaluaciones_positivas,
        'evaluaciones_negativas': evaluaciones_negativas,
        'porcentaje_positivo': (evaluaciones_positivas / total_evaluaciones * 100) if total_evaluaciones > 0 else 0
    }), 200 