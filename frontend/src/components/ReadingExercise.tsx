import React, { useState } from 'react';
import AudioRecorder from './AudioRecorder';
import ResultsView from './ResultsView';

interface ReadingExerciseProps {
  text: string;
  onComplete: (results: any) => void;
}

const ReadingExercise: React.FC<ReadingExerciseProps> = ({ text, onComplete }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [hasRecorded, setHasRecorded] = useState(false);
  const [showText, setShowText] = useState(false);
  const [step, setStep] = useState(1);
  const [results, setResults] = useState<any>(null);

  const handleStartRecording = () => {
    setShowText(true);
    setIsRecording(true);
    setStep(2);
  };

  const handleRecordingComplete = async (audioBlob: Blob) => {
    setHasRecorded(true);
    setIsRecording(false);
    setStep(3);

    const formData = new FormData();
    formData.append('audio', audioBlob, 'recording.wav');

    try {
      const response = await fetch('http://localhost:5000/api/audio/procesar', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      setResults(data);
      onComplete(data);
    } catch (error) {
      console.error('Error al procesar el audio:', error);
      setResults({ error: 'Error al procesar el audio. Por favor, intenta nuevamente.' });
    }
  };

  const resetExercise = () => {
    setShowText(false);
    setHasRecorded(false);
    setIsRecording(false);
    setStep(1);
    setResults(null);
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        <div className="bg-white rounded-xl shadow-lg overflow-hidden">
          {/* Encabezado */}
          <div className="bg-primary-600 px-6 py-4">
            <h2 className="text-2xl font-bold text-white">
              Ejercicio de Lectura
            </h2>
          </div>

          {/* Contenido principal */}
          <div className="p-6">
            {/* Indicador de progreso */}
            <div className="mb-8">
              <div className="flex items-center justify-between mb-2">
                <div className="flex space-x-2">
                  {[1, 2, 3].map((stepNumber) => (
                    <div
                      key={stepNumber}
                      className={`w-8 h-8 rounded-full flex items-center justify-center ${
                        step >= stepNumber
                          ? 'bg-primary-600 text-white'
                          : 'bg-gray-200 text-gray-600'
                      }`}
                    >
                      {stepNumber}
                    </div>
                  ))}
                </div>
                <span className="text-sm text-gray-500">
                  Paso {step} de 3
                </span>
              </div>
            </div>

            {/* Instrucciones iniciales */}
            {step === 1 && (
              <div className="space-y-6">
                <div className="bg-primary-50 p-4 rounded-lg">
                  <h3 className="text-lg font-semibold text-primary-800 mb-2">
                    Instrucciones:
                  </h3>
                  <ol className="list-decimal list-inside space-y-2 text-primary-700">
                    <li>Cuando estés listo, presiona "Comenzar Ejercicio"</li>
                    <li>Lee el texto que aparecerá en voz alta y clara</li>
                    <li>La grabación comenzará automáticamente</li>
                    <li>Al terminar, presiona "Detener Grabación"</li>
                  </ol>
                </div>
                <button
                  onClick={handleStartRecording}
                  className="w-full py-3 px-4 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-medium"
                >
                  Comenzar Ejercicio
                </button>
              </div>
            )}

            {/* Texto para leer y grabación */}
            {showText && !hasRecorded && (
              <div className="space-y-6">
                <div className={`transition-all duration-500 ${
                  isRecording ? 'bg-white' : 'bg-gray-50'
                } p-6 rounded-lg border-2 ${
                  isRecording ? 'border-primary-500' : 'border-gray-200'
                }`}>
                  <p className="text-lg leading-relaxed text-gray-800 font-serif">
                    {text}
                  </p>
                </div>

                <div className="mt-6">
                  <AudioRecorder
                    onRecordingComplete={handleRecordingComplete}
                    onStartRecording={() => setIsRecording(true)}
                    onStopRecording={() => setIsRecording(false)}
                  />
                </div>
              </div>
            )}

            {/* Resultados */}
            {results && (
              <div>
                <ResultsView results={results} />
                <button
                  onClick={resetExercise}
                  className="mt-6 w-full py-2 px-4 border border-primary-500 text-primary-600 rounded-lg hover:bg-primary-50 transition-colors"
                >
                  Realizar otro intento
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ReadingExercise; 