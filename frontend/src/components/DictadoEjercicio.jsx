import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Typography, 
  TextField, 
  Button, 
  Paper,
  CircularProgress,
  Alert
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const DictadoEjercicio = () => {
  const [audio, setAudio] = useState(null);
  const [palabrasDictado, setPalabrasDictado] = useState([]);
  const [textoUsuario, setTextoUsuario] = useState('');
  const [reproduciendo, setReproduciendo] = useState(false);
  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState(null);
  const [audioElement, setAudioElement] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const obtenerAudio = async () => {
      try {
        const response = await axios.get(
          'http://localhost:5000/api/v1/ejercicios/dictado',
          { responseType: 'blob' }
        );
        const palabrasHeader = response.headers['x-palabras-dictado'];
        setPalabrasDictado(palabrasHeader ? palabrasHeader.split(',') : []);
        const audioBlob = new Blob([response.data], { type: 'audio/mp3' });
        setAudio(URL.createObjectURL(audioBlob));
      } catch (error) {
        console.error('Error al obtener el audio:', error);
        setAudio(null);
        setError('No se pudo conectar con el servidor.');
      }
    };
    obtenerAudio();
    return () => {
      if (audioElement) {
        audioElement.pause();
        audioElement.src = '';
      }
      if (audio && audio.startsWith('blob:')) {
        URL.revokeObjectURL(audio);
      }
    };
    // eslint-disable-next-line
  }, []);

  const reproducirAudio = () => {
    if (!audio) return;
    if (audioElement) {
      audioElement.pause();
      audioElement.currentTime = 0;
    }
    const newAudioElement = new Audio(audio);
    setAudioElement(newAudioElement);
    setReproduciendo(true);
    setError(null);
    newAudioElement.play().catch(error => {
      console.error('Error al reproducir el audio:', error);
      setError('Error al reproducir el audio. Por favor, intente nuevamente.');
      setReproduciendo(false);
    });
    newAudioElement.onended = () => {
      setReproduciendo(false);
    };
  };

  const enviarRespuesta = async () => {
    if (!textoUsuario.trim()) {
      setError('Por favor, escriba las palabras antes de enviar.');
      return;
    }
    setCargando(true);
    setError(null);
    try {
      const palabrasUsuario = textoUsuario
        .split(/\s+/)
        .map(p => p.trim().toLowerCase())
        .filter(Boolean);
      const response = await axios.post(
        'http://localhost:5000/api/v1/ejercicios/dictado/evaluar',
        {
          texto_usuario: palabrasUsuario.join(' '),
          texto_original: palabrasDictado.join(' ')
        }
      );
      navigate('/resultados', { 
        state: { 
          resultados: response.data,
          tipo: 'dictado',
          palabras_usuario: palabrasUsuario,
          palabras_correctas: palabrasDictado
        }
      });
    } catch (error) {
      console.error('Error al enviar respuesta:', error);
      setError('Error al procesar la respuesta. Por favor, intente nuevamente.');
    } finally {
      setCargando(false);
    }
  };

  return (
    <Box sx={{ maxWidth: 800, margin: 'auto', padding: 4 }}>
      <Paper elevation={3} sx={{ padding: 3, marginBottom: 3 }}>
        <Typography variant="h4" gutterBottom>
          Ejercicio de Dictado
        </Typography>

        {error && (
          <Alert severity="info" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}
        <Typography variant="body1" paragraph>
          Escuche el audio y escriba las palabras dictadas en el orden correcto, separadas por espacio o salto de línea:
        </Typography>
        <Box sx={{ display: 'flex', justifyContent: 'center', marginY: 3 }}>
          <Button
            variant="contained"
            color="primary"
            onClick={reproducirAudio}
            disabled={!audio || reproduciendo}
            size="large"
          >
            {reproduciendo ? 'Reproduciendo...' : 'Reproducir Audio'}
          </Button>
        </Box>
        <TextField
          fullWidth
          multiline
          rows={3}
          variant="outlined"
          value={textoUsuario}
          onChange={(e) => setTextoUsuario(e.target.value)}
          placeholder="Escriba aquí las palabras dictadas..."
          sx={{ 
            marginY: 3,
            '& .MuiOutlinedInput-root': {
              fontSize: '1.1rem',
              lineHeight: '1.8'
            }
          }}
        />
        <Box sx={{ display: 'flex', justifyContent: 'center' }}>
          <Button
            variant="contained"
            color="primary"
            onClick={enviarRespuesta}
            disabled={!textoUsuario.trim() || cargando}
            size="large"
          >
            Enviar Respuesta
          </Button>
        </Box>
        {cargando && (
          <Box sx={{ display: 'flex', justifyContent: 'center', marginTop: 3 }}>
            <CircularProgress />
          </Box>
        )}
      </Paper>
    </Box>
  );
};

export default DictadoEjercicio;