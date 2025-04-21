from flask import Blueprint, request, jsonify
from .model import predict_dislexia
from .models import Evaluacion
from . import db
from datetime import datetime
from .utils import validar_datos_evaluacion, manejar_errores

api_blueprint = Blueprint("api", __name__)

@api_blueprint.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    try:
        resultado = predict_dislexia(data)

        nueva_eval = Evaluacion(
            tiempo_lectura=data["tiempo_lectura"],
            errores_escritura=data["errores_escritura"],
            comprension=data["comprension"],
            errores_dictado=data["errores_dictado"],
            respuestas_gramaticales=data["respuestas_gramaticales"],
            resultado=resultado
        )
        db.session.add(nueva_eval)
        db.session.commit()

        return jsonify({"prediction": resultado})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

main = Blueprint('main', __name__)

@main.route('/api/evaluaciones', methods=['POST'])
@manejar_errores
def crear_evaluacion():
    data = request.get_json()
    
    errores = validar_datos_evaluacion(data)
    if errores:
        return jsonify({'errores': errores}), 400
    
    nueva_evaluacion = Evaluacion(
        tiempo_lectura=data['tiempo_lectura'],
        errores_escritura=data['errores_escritura'],
        comprension=data['comprension'],
        errores_dictado=data['errores_dictado'],
        respuestas_gramaticales=data['respuestas_gramaticales'],
        prediccion=data['prediccion'],
        ip_address=request.remote_addr,
        user_agent=request.user_agent.string
    )
    
    db.session.add(nueva_evaluacion)
    db.session.commit()
    
    return jsonify({
        'mensaje': 'Evaluación creada exitosamente',
        'id': nueva_evaluacion.id
    }), 201

@main.route('/api/evaluaciones', methods=['GET'])
@manejar_errores
def obtener_evaluaciones():
    evaluaciones = Evaluacion.query.all()
    return jsonify([evaluacion.to_dict() for evaluacion in evaluaciones]), 200

@main.route('/api/evaluaciones/<int:id>', methods=['GET'])
@manejar_errores
def obtener_evaluacion(id):
    evaluacion = Evaluacion.query.get_or_404(id)
    return jsonify(evaluacion.to_dict()), 200

@main.route('/api/evaluaciones/<int:id>', methods=['DELETE'])
@manejar_errores
def eliminar_evaluacion(id):
    evaluacion = Evaluacion.query.get_or_404(id)
    db.session.delete(evaluacion)
    db.session.commit()
    return jsonify({'mensaje': 'Evaluación eliminada exitosamente'}), 200

@main.route('/api/estadisticas', methods=['GET'])
@manejar_errores
def obtener_estadisticas():
    total_evaluaciones = Evaluacion.query.count()
    evaluaciones_positivas = Evaluacion.query.filter_by(prediccion=1).count()
    evaluaciones_negativas = Evaluacion.query.filter_by(prediccion=0).count()
    
    return jsonify({
        'total_evaluaciones': total_evaluaciones,
        'evaluaciones_positivas': evaluaciones_positivas,
        'evaluaciones_negativas': evaluaciones_negativas,
        'porcentaje_positivo': (evaluaciones_positivas / total_evaluaciones * 100) if total_evaluaciones > 0 else 0
    }), 200
