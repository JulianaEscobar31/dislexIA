from typing import Dict, List, Optional
import random
import time
from datetime import datetime

class ExerciseService:
    def __init__(self):
        self.niveles_dificultad = {
            1: {'min_palabras': 50, 'max_palabras': 100},
            2: {'min_palabras': 100, 'max_palabras': 200},
            3: {'min_palabras': 200, 'max_palabras': 300}
        }
        
        self.tipos_ejercicios = [
            'lectura',
            'dictado',
            'comprension'
        ]
        
    def generar_ejercicio(self, tipo, nivel_dificultad=1):
        """Genera un ejercicio basado en el tipo y nivel de dificultad"""
        if tipo not in self.tipos_ejercicios:
            return {'error': 'Tipo de ejercicio no válido'}
            
        if nivel_dificultad not in self.niveles_dificultad:
            nivel_dificultad = 1
            
        ejercicio = {
            'tipo': tipo,
            'nivel': nivel_dificultad,
            'fecha_generacion': datetime.utcnow(),
            'contenido': self._generar_contenido(tipo, nivel_dificultad),
            'instrucciones': self._generar_instrucciones(tipo),
            'tiempo_estimado': self._calcular_tiempo_estimado(tipo, nivel_dificultad)
        }
        
        return ejercicio
        
    def _generar_contenido(self, tipo, nivel):
        """Genera el contenido específico para cada tipo de ejercicio"""
        if tipo == 'lectura':
            return self._generar_texto_lectura(nivel)
        elif tipo == 'dictado':
            return self._generar_texto_dictado(nivel)
        elif tipo == 'comprension':
            return self._generar_ejercicio_comprension(nivel)
            
    def _generar_texto_lectura(self, nivel):
        """Genera un texto para ejercicio de lectura"""
        textos = {
            1: [
                "El sol brillaba intensamente en el cielo azul mientras las nubes blancas flotaban perezosamente. Los pájaros cantaban alegres melodías y las flores se mecían suavemente con la brisa primaveral. Era un día perfecto para salir a pasear y disfrutar de la naturaleza.",
                "En el pequeño pueblo costero, los pescadores preparaban sus redes para otro día de trabajo en el mar. El aroma salado del océano llenaba el aire y las gaviotas volaban en círculos sobre los barcos anclados en el puerto."
            ],
            2: [
                "La antigua biblioteca guardaba secretos centenarios entre sus polvorientos estantes. Los libros, testigos silenciosos del paso del tiempo, contenían historias fascinantes que esperaban ser descubiertas por lectores curiosos. El bibliotecario, un hombre mayor de gafas redondas, conocía cada rincón y cada volumen como si fueran parte de su propia memoria.",
                "En el laboratorio de investigación, los científicos trabajaban incansablemente en busca de nuevos descubrimientos. Los microscopios zumbaban suavemente mientras las pantallas de las computadoras mostraban datos complejos. Cada experimento podría ser la clave para resolver importantes enigmas de la naturaleza."
            ],
            3: [
                "La revolución industrial transformó radicalmente la sociedad del siglo XIX, introduciendo cambios fundamentales en los métodos de producción y en la organización del trabajo. Las máquinas de vapor reemplazaron gradualmente el trabajo manual, las fábricas surgieron como nuevos centros de actividad económica, y las ciudades experimentaron un crecimiento sin precedentes mientras las personas migraban del campo en busca de oportunidades laborales.",
                "Los avances en la tecnología de la información han revolucionado la manera en que nos comunicamos y procesamos datos en el siglo XXI. La inteligencia artificial y el aprendizaje automático están transformando industrias enteras, mientras que la conectividad global instantánea ha creado nuevas formas de colaboración y compartir conocimientos."
            ]
        }
        
        return random.choice(textos[nivel])
        
    def _generar_texto_dictado(self, nivel):
        """Genera un texto para ejercicio de dictado"""
        textos = {
            1: [
                "La casa antigua tenía ventanas grandes y un jardín hermoso.",
                "Los niños jugaban felices en el parque durante la tarde."
            ],
            2: [
                "Durante el viaje, observamos paisajes increíbles y conocimos personas interesantes.",
                "El científico explicó su teoría sobre el cambio climático en la conferencia."
            ],
            3: [
                "La implementación de políticas sostenibles requiere la colaboración de múltiples sectores de la sociedad.",
                "Las investigaciones arqueológicas revelaron importantes hallazgos sobre civilizaciones antiguas."
            ]
        }
        
        return random.choice(textos[nivel])
        
    def _generar_ejercicio_comprension(self, nivel):
        """Genera un ejercicio de comprensión lectora"""
        ejercicios = {
            1: {
                'texto': "María disfruta mucho de la jardinería. Cada mañana riega sus plantas y les habla con cariño. Tiene rosas rojas, margaritas blancas y girasoles amarillos en su jardín.",
                'preguntas': [
                    {
                        'pregunta': "¿Qué hace María cada mañana?",
                        'opciones': ["Riega sus plantas", "Poda los árboles", "Planta nuevas flores"],
                        'respuesta_correcta': 0
                    },
                    {
                        'pregunta': "¿Qué tipos de flores tiene María en su jardín?",
                        'opciones': ["Solo rosas", "Rosas, margaritas y girasoles", "Margaritas y girasoles"],
                        'respuesta_correcta': 1
                    }
                ]
            },
            2: {
                'texto': "La contaminación plástica es uno de los mayores problemas ambientales actuales. Los océanos reciben toneladas de residuos plásticos cada año, afectando a la vida marina y los ecosistemas. Muchos países están implementando medidas para reducir el uso de plásticos de un solo uso.",
                'preguntas': [
                    {
                        'pregunta': "¿Cuál es el principal problema ambiental mencionado en el texto?",
                        'opciones': ["La deforestación", "La contaminación plástica", "El cambio climático"],
                        'respuesta_correcta': 1
                    },
                    {
                        'pregunta': "¿Qué están haciendo los países para abordar este problema?",
                        'opciones': ["Nada", "Aumentando la producción de plástico", "Reduciendo el uso de plásticos de un solo uso"],
                        'respuesta_correcta': 2
                    }
                ]
            },
            3: {
                'texto': "La inteligencia artificial está transformando diversos campos, desde la medicina hasta la educación. Los algoritmos de aprendizaje automático pueden analizar grandes cantidades de datos para identificar patrones y hacer predicciones. Sin embargo, también surgen preocupaciones éticas sobre la privacidad y el uso responsable de esta tecnología.",
                'preguntas': [
                    {
                        'pregunta': "¿Qué pueden hacer los algoritmos de aprendizaje automático?",
                        'opciones': ["Solo jugar ajedrez", "Analizar datos y hacer predicciones", "Reemplazar completamente a los humanos"],
                        'respuesta_correcta': 1
                    },
                    {
                        'pregunta': "¿Qué preocupaciones se mencionan en el texto?",
                        'opciones': ["Costo de la tecnología", "Privacidad y uso ético", "Velocidad de procesamiento"],
                        'respuesta_correcta': 1
                    },
                    {
                        'pregunta': "¿En qué campos está teniendo impacto la IA según el texto?",
                        'opciones': ["Solo en juegos", "En medicina y educación", "En deportes"],
                        'respuesta_correcta': 1
                    }
                ]
            }
        }
        
        return ejercicios[nivel]
        
    def _generar_instrucciones(self, tipo):
        """Genera instrucciones específicas para cada tipo de ejercicio"""
        instrucciones = {
            'lectura': "Lee el siguiente texto en voz alta. Trata de mantener un ritmo constante y pronunciar claramente cada palabra.",
            'dictado': "Escucha atentamente el texto que se te dictará y escríbelo. Presta atención a la ortografía y puntuación.",
            'comprension': "Lee el texto con atención y responde las preguntas. Selecciona la opción que mejor responda a cada pregunta."
        }
        
        return instrucciones[tipo]
        
    def _calcular_tiempo_estimado(self, tipo, nivel):
        """Calcula el tiempo estimado para completar el ejercicio"""
        tiempos_base = {
            'lectura': 5,
            'dictado': 8,
            'comprension': 10
        }
        
        # El tiempo aumenta con el nivel de dificultad
        return tiempos_base[tipo] * nivel
        
    def evaluar_respuesta(self, ejercicio, respuesta):
        """Evalúa la respuesta del usuario a un ejercicio"""
        if ejercicio['tipo'] == 'comprension':
            return self._evaluar_comprension(ejercicio, respuesta)
        elif ejercicio['tipo'] == 'dictado':
            return self._evaluar_dictado(ejercicio, respuesta)
        elif ejercicio['tipo'] == 'lectura':
            return self._evaluar_lectura(ejercicio, respuesta)
            
    def _evaluar_comprension(self, ejercicio, respuestas):
        """Evalúa las respuestas de comprensión lectora"""
        correctas = 0
        total_preguntas = len(ejercicio['contenido']['preguntas'])
        
        for i, respuesta in enumerate(respuestas):
            if respuesta == ejercicio['contenido']['preguntas'][i]['respuesta_correcta']:
                correctas += 1
                
        return {
            'puntuacion': (correctas / total_preguntas) * 100,
            'correctas': correctas,
            'total': total_preguntas
        }
        
    def _evaluar_dictado(self, ejercicio, respuesta):
        """Evalúa un ejercicio de dictado"""
        texto_original = ejercicio['contenido'].lower()
        respuesta = respuesta.lower()
        
        # Calcular similitud entre textos
        palabras_original = set(texto_original.split())
        palabras_respuesta = set(respuesta.split())
        
        palabras_correctas = len(palabras_original.intersection(palabras_respuesta))
        total_palabras = len(palabras_original)
        
        return {
            'puntuacion': (palabras_correctas / total_palabras) * 100,
            'palabras_correctas': palabras_correctas,
            'total_palabras': total_palabras
        }
        
    def _evaluar_lectura(self, ejercicio, datos_lectura):
        """Evalúa un ejercicio de lectura"""
        tiempo_esperado = self._calcular_tiempo_estimado(ejercicio['tipo'], ejercicio['nivel'])
        
        return {
            'tiempo_real': datos_lectura['tiempo'],
            'tiempo_esperado': tiempo_esperado,
            'fluidez': datos_lectura.get('palabras_por_minuto', 0),
            'precision': datos_lectura.get('precision', 0)
        }
        
    def ajustar_dificultad(self, historial_ejercicios):
        """Ajusta el nivel de dificultad basado en el rendimiento previo"""
        if not historial_ejercicios:
            return 1
            
        ultimas_evaluaciones = historial_ejercicios[-3:]
        promedio_puntuacion = sum(e['puntuacion'] for e in ultimas_evaluaciones) / len(ultimas_evaluaciones)
        
        if promedio_puntuacion > 85:
            return min(3, historial_ejercicios[-1]['nivel'] + 1)
        elif promedio_puntuacion < 60:
            return max(1, historial_ejercicios[-1]['nivel'] - 1)
        else:
            return historial_ejercicios[-1]['nivel']

    def _extraer_palabras_clave(self, texto: str) -> List[str]:
        # Implementar extracción real de palabras clave
        return [palabra for palabra in texto.split() if len(palabra) > 4]

exercise_service = ExerciseService() 