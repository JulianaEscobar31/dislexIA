import React from 'react';

interface ExerciseCardProps {
  title: string;
  description: string;
  icon: string;
  onClick: () => void;
}

const ExerciseCard: React.FC<ExerciseCardProps> = ({ title, description, icon, onClick }) => {
  return (
    <div 
      className="bg-white rounded-lg shadow-lg p-6 cursor-pointer transform transition-transform hover:scale-105"
      onClick={onClick}
    >
      <div className="text-4xl mb-4">{icon}</div>
      <h2 className="text-2xl font-semibold text-gray-800 mb-3">{title}</h2>
      <p className="text-gray-600">{description}</p>
      <button 
        className="mt-4 bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 transition-colors"
      >
        Comenzar
      </button>
    </div>
  );
};

export default ExerciseCard; 