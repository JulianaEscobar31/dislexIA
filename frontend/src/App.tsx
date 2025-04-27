import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import ReadingExercise from './components/ReadingExercise';
import './App.css'

const App: React.FC = () => {
  const textoLectura = `En un pequeño pueblo costero, María descubrió su pasión por la fotografía mientras 
  documentaba la vida cotidiana de los pescadores locales. Cada mañana, cuando el sol 
  apenas comenzaba a asomarse por el horizonte, ella capturaba imágenes de los botes 
  multicolores mecidos por las suaves olas del mar. Los pescadores, con sus rostros 
  curtidos por el sol y el salitre, le contaban historias fascinantes sobre sus 
  aventuras en alta mar. A través de su lente, María no solo registraba momentos, 
  sino que también preservaba la rica tradición marítima de su comunidad para las 
  generaciones futuras.`;

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route 
          path="/ejercicio/lectura" 
          element={
            <ReadingExercise 
              text={textoLectura}
              onComplete={(results) => {
                console.log('Resultados:', results);
                // TODO: Implementar visualización de resultados
              }}
            />
          } 
        />
        {/* TODO: Agregar rutas para los otros ejercicios */}
      </Routes>
    </Router>
  );
};

export default App;
