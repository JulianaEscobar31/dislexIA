from flask import Blueprint, request, jsonify
from ..services.evaluation_service import EvaluationService
from ..database.operations import obtener_todas_evaluaciones, generar_reporte_evaluaciones
from datetime import datetime

api = Blueprint('api', __name__)

@api.route('/evaluacion', methods=['POST'])
def crear_evaluacion():
    try:
        datos = request.get_json()
        resultado = EvaluationService.procesar_evaluacion(datos)
        return jsonify(resultado), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@api.route('/evaluacion/<int:id>', methods=['GET'])
def obtener_evaluacion(id):
    try:
        resultado = EvaluationService.obtener_resultado_evaluacion(id)
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@api.route('/evaluaciones', methods=['GET'])
def listar_evaluaciones():
    try:
        evaluaciones = obtener_todas_evaluaciones()
        return jsonify([eval.to_dict() for eval in evaluaciones]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@api.route('/reporte', methods=['GET'])
def obtener_reporte():
    try:
        fecha_inicio = request.args.get('fecha_inicio')
        fecha_fin = request.args.get('fecha_fin')
        
        if fecha_inicio:
            fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        if fecha_fin:
            fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')
            
        reporte = generar_reporte_evaluaciones(fecha_inicio, fecha_fin)
        return jsonify(reporte), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400 