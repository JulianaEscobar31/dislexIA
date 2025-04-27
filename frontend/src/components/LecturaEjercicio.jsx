import React, { useState, useEffect } from 'react';
import { Box, Button, Typography, Paper, CircularProgress } from '@mui/material';
import MicIcon from '@mui/icons-material/Mic';
import StopIcon from '@mui/icons-material/Stop';

const LecturaEjercicio = () => {
    const [texto, setTexto] = useState('');
    const [grabando, setGrabando] = useState(false);
    const [mediaRecorder, setMediaRecorder] = useState(null);
    const [resultado, setResultado] = useState(null);
    const [cargando, setCargando] = useState(false);

    useEffect(() => {
        // Obtener el texto de ejemplo al cargar el componente
        fetch('http://localhost:5000/api/texto-ejemplo')
            .then(response => response.json())
            .then(data => setTexto(data.texto))
            .catch(error => console.error('Error al obtener el texto:', error));
    }, []);

    const iniciarGrabacion = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            const recorder = new MediaRecorder(stream);
            const chunks = [];

            recorder.ondataavailable = (e) => chunks.push(e.data);
            recorder.onstop = async () => {
                const audioBlob = new Blob(chunks, { type: 'audio/wav' });
                await enviarAudio(audioBlob);
            };

            recorder.start();
            setMediaRecorder(recorder);
            setGrabando(true);
        } catch (error) {
            console.error('Error al iniciar la grabación:', error);
            alert('Error al acceder al micrófono. Por favor, asegúrate de dar permiso para usar el micrófono.');
        }
    };

    const detenerGrabacion = () => {
        if (mediaRecorder && mediaRecorder.state === 'recording') {
            mediaRecorder.stop();
            setGrabando(false);
        }
    };

    const enviarAudio = async (audioBlob) => {
        setCargando(true);
        const formData = new FormData();
        formData.append('audio', audioBlob);

        try {
            const response = await fetch('http://localhost:5000/api/audio/procesar', {
                method: 'POST',
                body: formData,
            });
            const data = await response.json();
            setResultado(data);
        } catch (error) {
            console.error('Error al procesar el audio:', error);
            alert('Error al procesar el audio. Por favor, intenta de nuevo.');
        } finally {
            setCargando(false);
        }
    };

    return (
        <Box sx={{ maxWidth: 800, margin: 'auto', padding: 3 }}>
            <Typography variant="h4" gutterBottom>
                Ejercicio de Lectura
            </Typography>

            <Paper elevation={3} sx={{ padding: 3, marginBottom: 3 }}>
                <Typography variant="h6" gutterBottom>
                    Instrucciones
                </Typography>
                <Typography paragraph>
                    Por favor, lee el siguiente texto en voz alta y clara:
                </Typography>
                <Typography 
                    paragraph 
                    sx={{ 
                        backgroundColor: '#f5f5f5',
                        padding: 2,
                        borderRadius: 1,
                        fontWeight: 'medium'
                    }}
                >
                    {texto}
                </Typography>
            </Paper>

            <Box sx={{ display: 'flex', justifyContent: 'center', gap: 2, marginBottom: 3 }}>
                <Button
                    variant="contained"
                    color={grabando ? "error" : "primary"}
                    startIcon={grabando ? <StopIcon /> : <MicIcon />}
                    onClick={grabando ? detenerGrabacion : iniciarGrabacion}
                    disabled={cargando}
                >
                    {grabando ? "Detener Grabación" : "Iniciar Grabación"}
                </Button>
            </Box>

            {cargando && (
                <Box sx={{ display: 'flex', justifyContent: 'center', marginY: 2 }}>
                    <CircularProgress />
                </Box>
            )}

            {resultado && (
                <Paper elevation={3} sx={{ padding: 3 }}>
                    <Typography variant="h6" gutterBottom>
                        Resultados
                    </Typography>
                    <Typography paragraph>
                        <strong>Texto transcrito:</strong> {resultado.texto}
                    </Typography>
                    <Typography paragraph>
                        <strong>Duración:</strong> {resultado.duracion.toFixed(2)} segundos
                    </Typography>
                    <Typography paragraph>
                        <strong>Palabras por minuto:</strong> {resultado.palabras_por_minuto.toFixed(2)}
                    </Typography>
                    <Typography paragraph>
                        <strong>Palabras totales:</strong> {resultado.palabras_totales}
                    </Typography>
                </Paper>
            )}
        </Box>
    );
};

export default LecturaEjercicio; 