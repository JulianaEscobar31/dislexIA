import React, { useState, useEffect, useRef } from 'react';
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

const DictadoEjercicio = (props) => {
  const [audio, setAudio] = useState(null);
  const [palabrasDictado, setPalabrasDictado] = useState([]);
  const [textoUsuario, setTextoUsuario] = useState('');
  const [reproduciendo, setReproduciendo] = useState(false);
  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState(null);
  const audioElementRef = useRef(null);
  const [dictadoId, setDictadoId] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    // Refuerzo: limpiar estado si no hay dictadoId o palabrasDictado válidos
    const palabrasGuardadas = localStorage.getItem('palabrasDictado');
    const dictadoIdGuardado = localStorage.getItem('dictadoId');
    if (!palabrasGuardadas || !dictadoIdGuardado) {
      setPalabrasDictado([]);
      setDictadoId('');
      setAudio(null);
      setError('Por favor, obtenga un nuevo dictado antes de continuar.');
    }
    const obtenerAudio = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/v1/ejercicios/dictado');
        if (!response.ok) {
          setError('No se pudo conectar con el servidor.');
          setAudio(null);
          return;
        }
        const contentType = response.headers.get('content-type');
        if (!contentType || !contentType.includes('audio')) {
          const text = await response.text();
          setError('Error del servidor: ' + text);
          setAudio(null);
          return;
        }
        const palabrasHeader = response.headers.get('x-palabras-dictado');
        const dictadoIdHeader = response.headers.get('x-dictado-id');
        const palabras = palabrasHeader ? palabrasHeader.split(',') : [];
        setPalabrasDictado(palabras);
        setDictadoId(dictadoIdHeader);
        localStorage.setItem('palabrasDictado', JSON.stringify(palabras));
        localStorage.setItem('dictadoId', dictadoIdHeader);
        const audioBlob = await response.blob();
        if (!audioBlob || audioBlob.size === 0) {
          setError('El audio recibido está vacío o es inválido. Intente nuevamente.');
          setAudio(null);
          return;
        }
        const audioUrl = URL.createObjectURL(audioBlob);
        setAudio(audioUrl);
        window.audioUrlDictado = audioUrl;
        console.log('Para probar el audio manualmente, ejecuta en la consola:');
        console.log('var audio = new Audio(window.audioUrlDictado); audio.play();');
      } catch (error) {
        console.error('Error al obtener el audio:', error);
        setAudio(null);
        setError('No se pudo conectar con el servidor.');
      }
    };
    obtenerAudio();
    return () => {
      if (audioElementRef.current) {
        audioElementRef.current.pause();
        audioElementRef.current.src = '';
      }
      if (audio && audio.startsWith('blob:')) {
        URL.revokeObjectURL(audio);
      }
      localStorage.removeItem('palabrasDictado');
      localStorage.removeItem('dictadoId');
    };
    // eslint-disable-next-line
  }, []);

  const reproducirAudio = () => {
    if (!audio) {
      setError('No se pudo cargar el audio. Intente nuevamente.');
      return;
    }
    if (audioElementRef.current) {
      audioElementRef.current.pause();
      audioElementRef.current.currentTime = 0;
    }
    const newAudioElement = new window.Audio(audio);
    audioElementRef.current = newAudioElement;
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
    if (palabrasDictado.length === 0 || !dictadoId) {
      setError('No se pudo obtener el dictado. Recargue la página e intente de nuevo.');
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
          dictado_id: dictadoId
        }
      );
      console.log('Respuesta del backend:', response.data);
      localStorage.removeItem('palabrasDictado');
      localStorage.removeItem('audioDictado');
      localStorage.removeItem('dictadoId');
      if (props.onFinish) {
        props.onFinish(response.data);
        return;
      }
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
      if (error.response && error.response.status === 400) {
        setError('El dictado expiró o ya fue evaluado. Avanzando al siguiente ejercicio...');
        setTimeout(() => {
          if (props.onFinish) {
            props.onFinish({ error: true });
          }
        }, 1500);
        return;
      }
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