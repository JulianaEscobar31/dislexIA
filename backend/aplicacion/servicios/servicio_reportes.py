import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64

class ServicioReportes:
    def __init__(self):
        self.metricas_base = {
            'tiempo_respuesta': [],
            'errores_ortograficos': [],
            'repeticiones': [],
            'comprension_lectora': [],
            'fecha_evaluacion': []
        }
        
    def generar_reporte_individual(self, datos_usuario):
        """Genera un reporte individual con gráficos y análisis"""
        try:
            df = pd.DataFrame(datos_usuario)
            
            reporte = {
                'metricas_generales': self._calcular_metricas_generales(df),
                'graficos': self._generar_graficos(df),
                'recomendaciones': self._generar_recomendaciones(df),
                'progreso': self._calcular_progreso(df)
            }
            
            return reporte
        except Exception as e:
            return {'error': f"Error generando reporte: {str(e)}"}
            
    def _calcular_metricas_generales(self, df):
        """Calcula métricas generales del usuario"""
        return {
            'promedio_tiempo_respuesta': df['tiempo_respuesta'].mean(),
            'total_errores': df['errores_ortograficos'].sum(),
            'promedio_comprension': df['comprension_lectora'].mean(),
            'total_evaluaciones': len(df),
            'ultima_evaluacion': df['fecha_evaluacion'].max()
        }
        
    def _generar_graficos(self, df):
        """Genera gráficos de progreso y rendimiento"""
        graficos = {}
        
        # Gráfico de progreso temporal
        plt.figure(figsize=(10, 6))
        plt.plot(df['fecha_evaluacion'], df['comprension_lectora'], marker='o')
        plt.title('Progreso en Comprensión Lectora')
        plt.xlabel('Fecha')
        plt.ylabel('Puntuación')
        plt.xticks(rotation=45)
        
        # Guardar gráfico en formato base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        graficos['progreso_temporal'] = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        # Gráfico de correlación
        plt.figure(figsize=(8, 8))
        sns.heatmap(df[['tiempo_respuesta', 'errores_ortograficos', 'comprension_lectora']].corr(),
                    annot=True, cmap='coolwarm')
        plt.title('Correlación entre Métricas')
        
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        graficos['correlacion'] = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return graficos
        
    def _generar_recomendaciones(self, df):
        """Genera recomendaciones personalizadas basadas en el rendimiento"""
        recomendaciones = []
        
        # Análisis de tiempo de respuesta
        tiempo_promedio = df['tiempo_respuesta'].mean()
        if tiempo_promedio > 30:
            recomendaciones.append(
                "Se recomienda practicar ejercicios de velocidad de lectura"
            )
            
        # Análisis de errores ortográficos
        errores_recientes = df['errores_ortograficos'].tail(3).mean()
        if errores_recientes > 5:
            recomendaciones.append(
                "Enfócate en ejercicios de escritura y dictado"
            )
            
        # Análisis de comprensión
        comprension_reciente = df['comprension_lectora'].tail(3).mean()
        if comprension_reciente < 0.7:
            recomendaciones.append(
                "Practica ejercicios de comprensión lectora con textos cortos"
            )
            
        return recomendaciones
        
    def _calcular_progreso(self, df):
        """Calcula el progreso del usuario en diferentes áreas"""
        if len(df) < 2:
            return {
                'mensaje': 'Se necesitan más evaluaciones para calcular el progreso'
            }
            
        primeras_eval = df.head(3)
        ultimas_eval = df.tail(3)
        
        progreso = {
            'tiempo_respuesta': {
                'cambio': (ultimas_eval['tiempo_respuesta'].mean() - 
                          primeras_eval['tiempo_respuesta'].mean()),
                'porcentaje': ((ultimas_eval['tiempo_respuesta'].mean() - 
                               primeras_eval['tiempo_respuesta'].mean()) / 
                              primeras_eval['tiempo_respuesta'].mean() * 100)
            },
            'errores_ortograficos': {
                'cambio': (ultimas_eval['errores_ortograficos'].mean() - 
                          primeras_eval['errores_ortograficos'].mean()),
                'porcentaje': ((ultimas_eval['errores_ortograficos'].mean() - 
                               primeras_eval['errores_ortograficos'].mean()) / 
                              primeras_eval['errores_ortograficos'].mean() * 100)
            },
            'comprension_lectora': {
                'cambio': (ultimas_eval['comprension_lectora'].mean() - 
                          primeras_eval['comprension_lectora'].mean()),
                'porcentaje': ((ultimas_eval['comprension_lectora'].mean() - 
                               primeras_eval['comprension_lectora'].mean()) / 
                              primeras_eval['comprension_lectora'].mean() * 100)
            }
        }
        
        return progreso

servicio_reportes = ServicioReportes() 