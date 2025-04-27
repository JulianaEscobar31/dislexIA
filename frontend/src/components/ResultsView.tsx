import React from 'react';

interface ResultsViewProps {
  results: {
    texto_transcrito?: string;
    metricas?: {
      duracion: number;
      intensidad_promedio: number;
      numero_pausas: number;
      fluidez: number;
    };
    error?: string;
  };
}

const ResultsView: React.FC<ResultsViewProps> = ({ results }) => {
  if (results.error) {
    return (
      <div className="bg-red-50 border-l-4 border-red-500 p-4 my-4">
        <div className="flex">
          <div className="flex-shrink-0">
            <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="ml-3">
            <h3 className="text-sm font-medium text-red-800">
              Error en el procesamiento
            </h3>
            <p className="mt-2 text-sm text-red-700">
              {results.error}
            </p>
          </div>
        </div>
      </div>
    );
  }

  if (!results.metricas || !results.texto_transcrito) {
    return null;
  }

  const { duracion, intensidad_promedio, numero_pausas, fluidez } = results.metricas;

  const getFluidezColor = (valor: number) => {
    if (valor >= 0.7) return 'text-green-600';
    if (valor >= 0.4) return 'text-yellow-600';
    return 'text-red-600';
  };

  const formatDuracion = (segundos: number) => {
    const minutos = Math.floor(segundos / 60);
    const segs = Math.round(segundos % 60);
    return `${minutos}:${segs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 mt-8">
      <h3 className="text-xl font-bold text-gray-800 mb-4">
        Resultados del Análisis
      </h3>

      <div className="mb-6">
        <h4 className="text-lg font-semibold text-gray-700 mb-2">
          Texto Transcrito:
        </h4>
        <div className="bg-gray-50 p-4 rounded-lg">
          <p className="text-gray-800 font-serif leading-relaxed">
            {results.texto_transcrito}
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-gray-50 p-4 rounded-lg">
          <h4 className="font-semibold text-gray-700 mb-2">Duración</h4>
          <p className="text-2xl font-bold text-primary-600">
            {formatDuracion(duracion)}
          </p>
          <p className="text-sm text-gray-500">minutos</p>
        </div>

        <div className="bg-gray-50 p-4 rounded-lg">
          <h4 className="font-semibold text-gray-700 mb-2">Pausas Detectadas</h4>
          <p className="text-2xl font-bold text-primary-600">
            {numero_pausas}
          </p>
          <p className="text-sm text-gray-500">total de pausas</p>
        </div>

        <div className="bg-gray-50 p-4 rounded-lg">
          <h4 className="font-semibold text-gray-700 mb-2">Intensidad Promedio</h4>
          <p className="text-2xl font-bold text-primary-600">
            {intensidad_promedio.toFixed(1)}
          </p>
          <p className="text-sm text-gray-500">dB</p>
        </div>

        <div className="bg-gray-50 p-4 rounded-lg">
          <h4 className="font-semibold text-gray-700 mb-2">Fluidez</h4>
          <p className={`text-2xl font-bold ${getFluidezColor(fluidez)}`}>
            {(fluidez * 100).toFixed(1)}%
          </p>
          <p className="text-sm text-gray-500">índice de fluidez</p>
        </div>
      </div>

      <div className="mt-6 p-4 bg-blue-50 rounded-lg">
        <h4 className="font-semibold text-blue-800 mb-2">
          Interpretación
        </h4>
        <p className="text-blue-700">
          {fluidez >= 0.7 
            ? "Tu lectura muestra una buena fluidez y naturalidad. ¡Excelente trabajo!"
            : fluidez >= 0.4
            ? "Tu lectura muestra algunas áreas de oportunidad. Considera practicar más para mejorar la fluidez."
            : "Se detectaron dificultades en la fluidez de la lectura. Te recomendamos practicar más y considerar una evaluación profesional."}
        </p>
      </div>
    </div>
  );
};

export default ResultsView; 