from flask import Blueprint, request, jsonify
from app.services.ml_service import predict_dislexia
from app.database.models import Evaluacion
from app import db
from datetime import datetime
from app.services.utils import validar_datos_evaluacion, manejar_errores

api = Blueprint('api', __name__)

@api.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    try:
        resultado = predict_dislexia(data)

        nueva_eval = Evaluacion(
            tiempo_respuesta=data["tiempo_respuesta"],
            errores_ortograficos=data["errores_ortograficos"],
            repeticiones=data["repeticiones"],
            comprension_lectora=data["comprension_lectora"],
            ejercicio_dictado=data["ejercicio_dictado"],
            ejercicio_lectura=data["ejercicio_lectura"],
            ejercicio_comprension=data["ejercicio_comprension"],
            prediccion=resultado["prediccion"],
            confianza_prediccion=resultado["confianza"]
        )
        db.session.add(nueva_eval)
        db.session.commit()

        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route('/api/evaluaciones', methods=['POST'])
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

@api.route('/api/evaluaciones', methods=['GET'])
@manejar_errores
def obtener_evaluaciones():
    evaluaciones = Evaluacion.query.all()
    return jsonify([evaluacion.to_dict() for evaluacion in evaluaciones]), 200

@api.route('/api/evaluaciones/<int:id>', methods=['GET'])
@manejar_errores
def obtener_evaluacion(id):
    evaluacion = Evaluacion.query.get_or_404(id)
    return jsonify(evaluacion.to_dict()), 200

@api.route('/api/evaluaciones/<int:id>', methods=['DELETE'])
@manejar_errores
def eliminar_evaluacion(id):
    evaluacion = Evaluacion.query.get_or_404(id)
    db.session.delete(evaluacion)
    db.session.commit()
    return jsonify({'mensaje': 'Evaluación eliminada exitosamente'}), 200

@api.route('/api/estadisticas', methods=['GET'])
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