import React, { useState, useEffect } from 'react';
import { Box, Typography, Button, Paper, CircularProgress, Alert } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import AudioRecorder from './AudioRecorder';

const LecturaEjercicio = (props) => {
    const [texto, setTexto] = useState('');
    const [grabando, setGrabando] = useState(false);
    const [audioBlob, setAudioBlob] = useState(null);
    const [cargando, setCargando] = useState(false);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        const obtenerTexto = async () => {
            try {
                const response = await axios.get('http://localhost:5000/api/v1/ejercicios/lectura');
                setTexto(response.data.texto);
            } catch (error) {
                console.error('Error al obtener el texto:', error);
                // Texto por defecto mientras se desarrolla el backend
                setTexto(`En un pequeño pueblo costero, María descubrió su pasión por la fotografía mientras documentaba la vida cotidiana de los pescadores locales. Cada mañana, cuando el sol apenas comenzaba a asomarse por el horizonte, ella capturaba imágenes de los botes multicolores mecidos por las suaves olas del mar. Los pescadores, con sus rostros curtidos por el sol y el salitre, le contaban historias fascinantes sobre sus aventuras en alta mar.`);
                setError('No se pudo conectar con el servidor. Usando texto de prueba.');
            }
        };
        obtenerTexto();
    }, []);

    const manejarInicioGrabacion = () => {
        setGrabando(true);
        setError(null);
    };

    const manejarFinGrabacion = async (blob) => {
        setAudioBlob(blob);
        setGrabando(false);
        setCargando(true);

        const formData = new FormData();
        formData.append('audio', blob, 'grabacion.wav');
        formData.append('texto_original', texto);

        try {
            const response = await axios.post(
                'http://localhost:5000/api/v1/ejercicios/lectura/evaluar',
                formData,
                {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    },
                }
            );
            
            if (props.onFinish) {
                props.onFinish(response.data);
                return;
            }
            navigate('/resultados', { 
                state: { 
                    resultados: response.data,
                    tipo: 'lectura'
                }
            });
        } catch (error) {
            console.error('Error al enviar el audio:', error);
            setError('Error al procesar el audio. Por favor, intente nuevamente.');
        } finally {
            setCargando(false);
        }
    };

    return (
        <Box sx={{ maxWidth: 800, margin: 'auto', padding: 4 }}>
            <Paper elevation={3} sx={{ padding: 3, marginBottom: 3 }}>
                <Typography variant="h4" gutterBottom>
                    Ejercicio de Lectura
                </Typography>
                
                {error && (
                    <Alert severity="info" sx={{ mb: 2 }}>
                        {error}
                    </Alert>
                )}

                <Typography variant="body1" paragraph>
                    Por favor, lea el siguiente texto en voz alta:
                </Typography>
                <Typography 
                    variant="body1" 
                    className="readable-text"
                    sx={{ 
                        backgroundColor: '#f5f5f5',
                        padding: 2,
                        borderRadius: 1,
                        marginBottom: 3,
                        fontFamily: "'Georgia', serif",
                        fontSize: '1.2rem',
                        lineHeight: '1.8'
                    }}
                >
                    {texto}
                </Typography>
                
                <Box sx={{ display: 'flex', justifyContent: 'center', gap: 2 }}>
                    {!grabando && !audioBlob && (
                        <Button
                            variant="contained"
                            color="primary"
                            onClick={manejarInicioGrabacion}
                            size="large"
                        >
                            Comenzar Grabación
                        </Button>
                    )}
                    
                    {grabando && (
                        <AudioRecorder
                            onStop={manejarFinGrabacion}
                            onStart={() => setGrabando(true)}
                        />
                    )}
                </Box>

                {cargando && (
                    <Box sx={{ display: 'flex', justifyContent: 'center', mt: 3 }}>
                        <CircularProgress />
                    </Box>
                )}
            </Paper>
        </Box>
    );
};

export default LecturaEjercicio; 