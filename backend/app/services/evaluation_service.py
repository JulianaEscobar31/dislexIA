from ..database.operations import guardar_evaluacion, obtener_evaluacion
from ..ml.predictor import predecir_dislexia

class EvaluationService:
    @staticmethod
    def procesar_evaluacion(datos_evaluacion):
        """Procesa una evaluación completa"""
        try:
            # Realizar predicción
            resultado_prediccion = predecir_dislexia(datos_evaluacion)
            
            # Agregar predicción a los datos
            datos_evaluacion['prediccion'] = resultado_prediccion['prediccion']
            
            # Guardar en base de datos
            evaluacion_id = guardar_evaluacion(datos_evaluacion)
            
            return {
                'id': evaluacion_id,
                'resultado': resultado_prediccion
            }
        except Exception as e:
            raise Exception(f"Error al procesar la evaluación: {str(e)}")

    @staticmethod
    def obtener_resultado_evaluacion(evaluacion_id):
        """Obtiene el resultado de una evaluación específica"""
        try:
            evaluacion = obtener_evaluacion(evaluacion_id)
            return evaluacion.to_dict()
        except Exception as e:
            raise Exception(f"Error al obtener la evaluación: {str(e)}") 