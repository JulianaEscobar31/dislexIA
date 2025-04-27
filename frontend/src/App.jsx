import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LecturaEjercicio from './components/LecturaEjercicio';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/ejercicio-lectura" element={<LecturaEjercicio />} />
      </Routes>
    </Router>
  );
}

export default App; 