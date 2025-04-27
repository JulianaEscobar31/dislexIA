import React from 'react';
import { useNavigate } from 'react-router-dom';
import ExerciseCard from '../components/ExerciseCard';

const Home: React.FC = () => {
  const navigate = useNavigate();

  const exercises = [
    {
      id: 'lectura',
      title: 'Ejercicio de Lectura',
      description: 'Lee un texto en voz alta mientras grabamos tu voz para analizar la fluidez y patrones de lectura.',
      icon: '📖'
    },
    {
      id: 'dictado',
      title: 'Ejercicio de Dictado',
      description: 'Escucha y escribe el texto dictado para evaluar tu capacidad de procesamiento auditivo y escritura.',
      icon: '✍️'
    },
    {
      id: 'comprension',
      title: 'Comprensión Lectora',
      description: 'Lee un texto y responde preguntas para evaluar tu comprensión y retención de información.',
      icon: '🤔'
    }
  ];

  return (
    <div className="container mx-auto px-4 py-8">
      <header className="text-center mb-12">
        <h1 className="text-4xl font-bold text-gray-800 mb-4">
          Evaluación de Dislexia
        </h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          Realiza los siguientes ejercicios para evaluar tus habilidades de lectura, escritura y comprensión.
        </p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {exercises.map((exercise) => (
          <ExerciseCard
            key={exercise.id}
            title={exercise.title}
            description={exercise.description}
            icon={exercise.icon}
            onClick={() => navigate(`/ejercicio/${exercise.id}`)}
          />
        ))}
      </div>

      <footer className="mt-16 text-center text-gray-600">
        <p>
          Esta herramienta está diseñada para ayudar en la detección temprana de patrones asociados con la dislexia.
          No constituye un diagnóstico médico.
        </p>
      </footer>
    </div>
  );
};

export default Home; 