import React, { useState } from 'react';
import DictadoEjercicio from './DictadoEjercicio';
import LecturaEjercicio from './LecturaEjercicio';
import ComprensionEjercicio from './ComprensionEjercicio';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const TestFlow = () => {
  const [paso, setPaso] = useState(0);
  const [resultados, setResultados] = useState({});
  const navigate = useNavigate();

  const handleSiguiente = async (tipo, resultado) => {
    const nuevosResultados = { ...resultados, [tipo]: resultado };
    setResultados(nuevosResultados);
    if (paso === 2) {
      // Al terminar todos los ejercicios, enviar al backend para análisis global
      try {
        const response = await axios.post('http://localhost:5000/api/v1/ejercicios/analisis_global', nuevosResultados);
        navigate('/resultados', { state: { resumen: nuevosResultados, analisisGlobal: response.data } });
      } catch (error) {
        navigate('/resultados', { state: { resumen: nuevosResultados, analisisGlobal: { error: 'No se pudo obtener el análisis global.' } } });
      }
    } else {
      setPaso(paso + 1);
    }
  };

  return (
    <div>
      {paso === 0 && (
        <DictadoEjercicio onFinish={res => handleSiguiente('dictado', res)} />
      )}
      {paso === 1 && (
        <LecturaEjercicio onFinish={res => handleSiguiente('lectura', res)} />
      )}
      {paso === 2 && (
        <ComprensionEjercicio onFinish={res => handleSiguiente('comprension', res)} />
      )}
    </div>
  );
};

export default TestFlow; 