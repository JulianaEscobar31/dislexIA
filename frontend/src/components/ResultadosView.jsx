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

  // Asegurar que los datos del gráfico sean números válidos
  const precision = Number(resultados.precision) || 0;
  const fluidez = Number(resultados.fluidez) || 0;
  const comprension = Number(resultados.comprension) || 0;

  const datosGrafica = {
    labels: ['Precisión', 'Fluidez', 'Comprensión'],
    datasets: [
      {
        label: 'Puntuación',
        data: [precision, fluidez, comprension],
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

  // Filtrar recomendaciones válidas
  const recomendacionesValidas = (resultados.recomendaciones || []).filter(r => r && r.trim() !== '');

  // Obtener palabras correctas y del usuario desde location.state o resultados
  const palabrasUsuario = (location.state?.palabras_usuario && location.state.palabras_usuario.length > 0)
    ? location.state.palabras_usuario
    : (resultados.palabras_usuario || []);
  const palabrasCorrectas = (location.state?.palabras_correctas && location.state.palabras_correctas.length > 0)
    ? location.state.palabras_correctas
    : (resultados.palabras_correctas || []);

  return (
    <Box sx={{ maxWidth: 800, margin: 'auto', padding: 4 }}>
      <Paper elevation={3} sx={{ padding: 3, marginBottom: 3 }}>
        <Typography variant="h4" gutterBottom>
          {tipo === 'lectura' && 'Resultados del Ejercicio de Lectura'}
          {tipo === 'dictado' && 'Resultados del Ejercicio de Dictado'}
          {tipo === 'comprension' && 'Resultados del Ejercicio de Comprensión Lectora'}
        </Typography>

        <Box sx={{ marginY: 4 }}>
          {tipo === 'comprension' ? (
            <>
              <Typography variant="body1" gutterBottom>
                Respuestas correctas: {resultados.correctas ?? 0} / {resultados.total ?? 0}
              </Typography>
            </>
          ) : (
            <>
              <Typography variant="h6" gutterBottom>
                Puntuación General: {Number(resultados.puntuacion_general).toFixed(1)}%
              </Typography>
              <LinearProgress 
                variant="determinate" 
                value={Number(resultados.puntuacion_general)} 
                sx={{ height: 10, borderRadius: 5 }}
              />
            </>
          )}
        </Box>

        {/* Mostrar texto original y transcrito si existen */}
        {resultados.texto_original && resultados.texto_transcrito && (
          <Box sx={{ marginY: 4 }}>
            <Typography variant="subtitle1" gutterBottom>
              <b>Texto Original:</b>
            </Typography>
            <Paper sx={{ padding: 2, backgroundColor: '#f5f5f5', marginBottom: 2 }}>
              <Typography variant="body1" sx={{ fontFamily: 'Georgia, serif' }}>
                {resultados.texto_original}
              </Typography>
            </Paper>
            <Typography variant="subtitle1" gutterBottom>
              <b>Texto Leído (Transcrito):</b>
            </Typography>
            <Paper sx={{ padding: 2, backgroundColor: '#f5f5f5' }}>
              <Typography variant="body1" sx={{ fontFamily: 'Georgia, serif' }}>
                {resultados.texto_transcrito}
              </Typography>
            </Paper>
          </Box>
        )}

        {/* Mostrar texto original y transcrito si existen */}
        {tipo === 'dictado' && palabrasUsuario.length > 0 && palabrasCorrectas.length > 0 && (
          <Box sx={{ marginY: 4 }}>
            <Typography variant="subtitle1" gutterBottom>
              <b>Comparación de Palabras:</b>
            </Typography>
            <Paper sx={{ padding: 2, backgroundColor: '#f5f5f5' }}>
              <Grid container spacing={2}>
                {palabrasCorrectas.map((palabra, index) => (
                  <Grid item xs={12} key={index}>
                    <Box sx={{ 
                      display: 'flex', 
                      alignItems: 'center',
                      backgroundColor: palabrasUsuario[index] === palabra ? '#e8f5e9' : '#ffebee',
                      padding: 1,
                      borderRadius: 1
                    }}>
                      <Typography variant="body1" sx={{ minWidth: 100 }}>
                        <b>Palabra {index + 1}:</b>
                      </Typography>
                      <Typography variant="body1" sx={{ flex: 1 }}>
                        <b>Correcta:</b> {palabra}
                      </Typography>
                      <Typography variant="body1" sx={{ flex: 1 }}>
                        <b>Tu respuesta:</b> {palabrasUsuario[index] || 'No escrita'}
                      </Typography>
                    </Box>
                  </Grid>
                ))}
              </Grid>
            </Paper>
          </Box>
        )}

        {/* Mostrar gráfica solo si no es comprensión */}
        {tipo !== 'comprension' && (
          <Box sx={{ height: 300, marginY: 4 }}>
            <Bar data={datosGrafica} options={opcionesGrafica} />
          </Box>
        )}

        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Typography variant="h6" gutterBottom>
              Detalles del Análisis
            </Typography>
            <List>
              {tipo === 'comprension' ? (
                <ListItem>
                  <ListItemText primary="¡Buen trabajo! Revisa tus respuestas y sigue practicando la comprensión lectora." />
                </ListItem>
              ) : (
                resultados.detalles_analisis?.map((detalle, index) => (
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
                ))
              )}
            </List>
          </Grid>

          <Grid item xs={12} md={6}>
            <Typography variant="h6" gutterBottom>
              Recomendaciones
            </Typography>
            <List>
              {recomendacionesValidas.length > 0 ? (
                recomendacionesValidas.map((recomendacion, index) => (
                  <ListItem key={index}>
                    <ListItemIcon>
                      <InfoIcon color="primary" />
                    </ListItemIcon>
                    <ListItemText primary={recomendacion} />
                  </ListItem>
                ))
              ) : (
                <ListItem>
                  <ListItemText primary="No hay recomendaciones disponibles." />
                </ListItem>
              )}
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