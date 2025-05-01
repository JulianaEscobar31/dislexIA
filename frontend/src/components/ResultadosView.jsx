import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import {
  Box,
  Paper,
  Typography,
  Button,
  Grid,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  LinearProgress
} from '@mui/material';
import InfoIcon from '@mui/icons-material/Info';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ErrorIcon from '@mui/icons-material/Error';
import { 
  Chart as ChartJS, 
  CategoryScale, 
  LinearScale, 
  BarElement, 
  Title, 
  Tooltip, 
  Legend 
} from 'chart.js';
import { Bar } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const ResultadosView = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { resultados, tipo } = location.state || {};

  if (!resultados) {
    return (
      <Box sx={{ maxWidth: 800, margin: 'auto', padding: 4 }}>
        <Typography variant="h4" color="error">
          No hay resultados disponibles
        </Typography>
        <Button 
          variant="contained" 
          onClick={() => navigate('/')}
          sx={{ marginTop: 2 }}
        >
          Volver al Inicio
        </Button>
      </Box>
    );
  }

  const datosGrafica = {
    labels: ['Precisión', 'Fluidez', 'Comprensión'],
    datasets: [
      {
        label: 'Puntuación',
        data: [
          resultados.precision || 0,
          resultados.fluidez || 0,
          resultados.comprension || 0
        ],
        backgroundColor: [
          'rgba(54, 162, 235, 0.6)',
          'rgba(75, 192, 192, 0.6)',
          'rgba(153, 102, 255, 0.6)'
        ],
        borderColor: [
          'rgba(54, 162, 235, 1)',
          'rgba(75, 192, 192, 1)',
          'rgba(153, 102, 255, 1)'
        ],
        borderWidth: 1
      }
    ]
  };

  const opcionesGrafica = {
    responsive: true,
    plugins: {
      legend: {
        display: false
      },
      title: {
        display: true,
        text: 'Análisis de Desempeño'
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 100,
        ticks: {
          callback: (value) => `${value}%`
        }
      }
    }
  };

  return (
    <Box sx={{ maxWidth: 800, margin: 'auto', padding: 4 }}>
      <Paper elevation={3} sx={{ padding: 3, marginBottom: 3 }}>
        <Typography variant="h4" gutterBottom>
          Resultados del Ejercicio de {tipo === 'lectura' ? 'Lectura' : 'Dictado'}
        </Typography>

        <Box sx={{ marginY: 4 }}>
          <Typography variant="h6" gutterBottom>
            Puntuación General: {resultados.puntuacion_general}%
          </Typography>
          <LinearProgress 
            variant="determinate" 
            value={resultados.puntuacion_general} 
            sx={{ height: 10, borderRadius: 5 }}
          />
        </Box>

        <Box sx={{ height: 300, marginY: 4 }}>
          <Bar data={datosGrafica} options={opcionesGrafica} />
        </Box>

        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Typography variant="h6" gutterBottom>
              Detalles del Análisis
            </Typography>
            <List>
              {resultados.detalles_analisis?.map((detalle, index) => (
                <ListItem key={index}>
                  <ListItemIcon>
                    {detalle.cumplido ? (
                      <CheckCircleIcon color="success" />
                    ) : (
                      <ErrorIcon color="error" />
                    )}
                  </ListItemIcon>
                  <ListItemText primary={detalle.descripcion} />
                </ListItem>
              ))}
            </List>
          </Grid>

          <Grid item xs={12} md={6}>
            <Typography variant="h6" gutterBottom>
              Recomendaciones
            </Typography>
            <List>
              {resultados.recomendaciones?.map((recomendacion, index) => (
                <ListItem key={index}>
                  <ListItemIcon>
                    <InfoIcon color="primary" />
                  </ListItemIcon>
                  <ListItemText primary={recomendacion} />
                </ListItem>
              ))}
            </List>
          </Grid>
        </Grid>

        <Box sx={{ display: 'flex', justifyContent: 'center', marginTop: 4 }}>
          <Button 
            variant="contained" 
            onClick={() => navigate('/')}
            sx={{ marginRight: 2 }}
          >
            Volver al Inicio
          </Button>
          <Button 
            variant="outlined" 
            onClick={() => navigate(`/${tipo}`)}
          >
            Intentar Otro Ejercicio
          </Button>
        </Box>
      </Paper>
    </Box>
  );
};

export default ResultadosView; 