import React, { useState, useEffect } from 'react';
import { Box, IconButton, Typography } from '@mui/material';
import MicIcon from '@mui/icons-material/Mic';
import StopIcon from '@mui/icons-material/Stop';

const AudioRecorder = ({ onStart, onStop }) => {
  const [mediaRecorder, setMediaRecorder] = useState(null);
  const [audioChunks, setAudioChunks] = useState([]);
  const [tiempoGrabacion, setTiempoGrabacion] = useState(0);
  const [intervalId, setIntervalId] = useState(null);

  useEffect(() => {
    return () => {
      if (intervalId) {
        clearInterval(intervalId);
      }
      if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        mediaRecorder.stop();
      }
    };
  }, [mediaRecorder, intervalId]);

  const iniciarGrabacion = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      const chunks = [];

      recorder.ondataavailable = (e) => {
        if (e.data.size > 0) {
          chunks.push(e.data);
        }
      };

      recorder.onstop = () => {
        const audioBlob = new Blob(chunks, { type: 'audio/wav' });
        stream.getTracks().forEach(track => track.stop());
        if (intervalId) {
          clearInterval(intervalId);
          setIntervalId(null);
        }
        onStop(audioBlob);
      };

      setAudioChunks(chunks);
      setMediaRecorder(recorder);
      
      recorder.start();
      onStart();

      const id = setInterval(() => {
        setTiempoGrabacion(prev => prev + 1);
      }, 1000);
      setIntervalId(id);
    } catch (error) {
      console.error('Error al iniciar la grabación:', error);
    }
  };

  const detenerGrabacion = () => {
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
      mediaRecorder.stop();
    }
  };

  const formatearTiempo = (segundos) => {
    const minutos = Math.floor(segundos / 60);
    const segs = segundos % 60;
    return `${minutos.toString().padStart(2, '0')}:${segs.toString().padStart(2, '0')}`;
  };

  return (
    <Box sx={{ 
      display: 'flex', 
      flexDirection: 'column', 
      alignItems: 'center',
      gap: 2 
    }}>
      <Typography variant="h6">
        {formatearTiempo(tiempoGrabacion)}
      </Typography>
      
      {!mediaRecorder && (
        <IconButton 
          color="primary" 
          onClick={iniciarGrabacion}
          sx={{ 
            width: 56,
            height: 56,
            backgroundColor: 'primary.main',
            color: 'white',
            '&:hover': {
              backgroundColor: 'primary.dark',
            }
          }}
        >
          <MicIcon />
        </IconButton>
      )}

      {mediaRecorder && (
        <IconButton 
          color="error" 
          onClick={detenerGrabacion}
          sx={{ 
            width: 56,
            height: 56,
            backgroundColor: 'error.main',
            color: 'white',
            '&:hover': {
              backgroundColor: 'error.dark',
            }
          }}
        >
          <StopIcon />
        </IconButton>
      )}
    </Box>
  );
};

export default AudioRecorder; 