import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Box, Button, Typography, Paper } from '@mui/material';

const Inicio = () => {
  const navigate = useNavigate();
  return (
    <Box sx={{ maxWidth: 500, margin: 'auto', padding: 4, minHeight: '60vh', display: 'flex', alignItems: 'center' }}>
      <Paper elevation={3} sx={{ padding: 4, width: '100%' }}>
        <Typography variant="h3" gutterBottom align="center">
          ¡Bienvenido a la Evaluación de Dislexia!
        </Typography>
        <Typography variant="body1" align="center" sx={{ marginBottom: 4 }}>
          Esta prueba interactiva evalúa tus habilidades de lectura, escritura y comprensión mediante ejercicios personalizados. Haz clic en el botón para comenzar.
        </Typography>
        <Box sx={{ display: 'flex', justifyContent: 'center' }}>
          <Button variant="contained" color="primary" size="large" onClick={() => navigate('/test')}>
            Iniciar Test
          </Button>
        </Box>
      </Paper>
    </Box>
  );
};

export default Inicio; 