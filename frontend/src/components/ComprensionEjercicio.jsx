import React, { useState, useEffect } from 'react';
import { Box, Typography, Button, Paper, CircularProgress, Alert, Radio, RadioGroup, FormControlLabel } from '@mui/material';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const ComprensionEjercicio = () => {
  const [ejercicio, setEjercicio] = useState(null);
  const [respuestas, setRespuestas] = useState({});
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState(null);
  const [enviando, setEnviando] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const obtenerEjercicio = async () => {
      setCargando(true);
      try {
        const response = await axios.get('http://localhost:5000/api/v1/ejercicios/comprension');
        setEjercicio(response.data);
      } catch (err) {
        setError('No se pudo obtener el ejercicio de comprensión lectora.');
      } finally {
        setCargando(false);
      }
    };
    obtenerEjercicio();
  }, []);

  const handleRespuesta = (preguntaIdx, opcionIdx) => {
    setRespuestas({ ...respuestas, [preguntaIdx]: opcionIdx });
  };

  const enviarRespuestas = async () => {
    setEnviando(true);
    setError(null);
    try {
      const response = await axios.post('http://localhost:5000/api/v1/ejercicios/comprension/evaluar', {
        nivel: ejercicio.nivel || 'nivel_1',
        respuestas: Object.values(respuestas),
        tiempo_respuesta: 0
      });
      navigate('/resultados', {
        state: {
          resultados: response.data,
          tipo: 'comprension'
        }
      });
    } catch (err) {
      setError('Error al enviar las respuestas.');
    } finally {
      setEnviando(false);
    }
  };

  if (cargando) {
    return <Box sx={{ display: 'flex', justifyContent: 'center', mt: 6 }}><CircularProgress /></Box>;
  }

  if (error) {
    return <Alert severity="error">{error}</Alert>;
  }

  if (!ejercicio) {
    return null;
  }

  return (
    <Box sx={{ maxWidth: 800, margin: 'auto', padding: 4 }}>
      <Paper elevation={3} sx={{ padding: 3, marginBottom: 3 }}>
        <Typography variant="h4" gutterBottom>
          Comprensión Lectora
        </Typography>
        <Typography variant="body1" paragraph>
          {ejercicio.texto}
        </Typography>
        {ejercicio.preguntas && ejercicio.preguntas.map((pregunta, idx) => (
          <Box key={idx} sx={{ mb: 3 }}>
            <Typography variant="subtitle1" gutterBottom>
              {pregunta.pregunta}
            </Typography>
            <RadioGroup
              value={respuestas[idx] ?? ''}
              onChange={e => handleRespuesta(idx, Number(e.target.value))}
            >
              {pregunta.opciones.map((opcion, oidx) => (
                <FormControlLabel
                  key={oidx}
                  value={oidx}
                  control={<Radio />}
                  label={opcion}
                />
              ))}
            </RadioGroup>
          </Box>
        ))}
        <Button
          variant="contained"
          color="primary"
          onClick={enviarRespuestas}
          disabled={enviando || Object.keys(respuestas).length !== (ejercicio.preguntas?.length || 0)}
        >
          Enviar Respuestas
        </Button>
      </Paper>
    </Box>
  );
};

export default ComprensionEjercicio; 