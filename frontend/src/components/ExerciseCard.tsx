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
      className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow cursor-pointer"
      onClick={onClick}
    >
      <div className="flex items-center mb-4">
        <span className="text-3xl mr-4">{icon}</span>
        <h3 className="text-xl font-semibold text-gray-800">{title}</h3>
      </div>
      <p className="text-gray-600">{description}</p>
    </div>
  );
};

export default ExerciseCard; 