import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';

interface ReadingExerciseProps {
  text: string;
  onComplete: (results: any) => void;
}

const ReadingExercise: React.FC<ReadingExerciseProps> = ({ text, onComplete }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [hasStarted, setHasStarted] = useState(false);
  const [timeElapsed, setTimeElapsed] = useState(0);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const timerRef = useRef<number | null>(null);
  const navigate = useNavigate();

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      const audioChunks: BlobPart[] = [];

      mediaRecorder.ondataavailable = (event) => {
        audioChunks.push(event.data);
      };

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        const audioUrl = URL.createObjectURL(audioBlob);
        
        // Aquí enviarías el audio al backend para su análisis
        onComplete({
          audioUrl,
          timeElapsed,
          // Otros datos relevantes
        });
      };

      mediaRecorderRef.current = mediaRecorder;
      mediaRecorder.start();
      setIsRecording(true);
      setHasStarted(true);

      // Iniciar el temporizador
      timerRef.current = window.setInterval(() => {
        setTimeElapsed(prev => prev + 1);
      }, 1000);

    } catch (error) {
      console.error('Error al acceder al micrófono:', error);
      alert('No se pudo acceder al micrófono. Por favor, verifica los permisos.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
      setIsRecording(false);
      
      if (timerRef.current !== null) {
        window.clearInterval(timerRef.current);
      }
    }
  };

  return (
    <div className="container mx-auto px-4 py-8 max-w-3xl">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">
        Ejercicio de Lectura
      </h1>

      <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
        <div className="mb-6">
          <h2 className="text-xl font-semibold text-gray-700 mb-4">
            Instrucciones
          </h2>
          <p className="text-gray-600">
            Lee el siguiente texto en voz alta y clara. Presiona "Comenzar" cuando estés listo 
            para empezar la grabación y "Terminar" cuando hayas terminado de leer.
          </p>
        </div>

        <div className="bg-gray-50 p-6 rounded-md mb-6">
          <p className="text-lg leading-relaxed whitespace-pre-line">
            {text}
          </p>
        </div>

        <div className="flex justify-between items-center">
          <div className="text-gray-600">
            Tiempo: {Math.floor(timeElapsed / 60)}:{(timeElapsed % 60).toString().padStart(2, '0')}
          </div>
          
          {!hasStarted ? (
            <button
              onClick={startRecording}
              className="bg-green-500 text-white px-6 py-2 rounded-md hover:bg-green-600 transition-colors"
            >
              Comenzar
            </button>
          ) : (
            <button
              onClick={stopRecording}
              className="bg-red-500 text-white px-6 py-2 rounded-md hover:bg-red-600 transition-colors"
              disabled={!isRecording}
            >
              Terminar
            </button>
          )}
        </div>
      </div>

      <div className="flex justify-between">
        <button
          onClick={() => navigate('/')}
          className="text-gray-600 hover:text-gray-800"
        >
          ← Volver al inicio
        </button>
      </div>
    </div>
  );
};

export default ReadingExercise; 