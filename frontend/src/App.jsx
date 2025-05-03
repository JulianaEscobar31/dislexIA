import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { 
  Box, 
  AppBar, 
  Toolbar, 
  Typography, 
  Container, 
  Button, 
  Paper,
  Grid,
  Card,
  CardContent,
  CardActions
} from '@mui/material';
import LecturaEjercicio from './components/LecturaEjercicio';
import DictadoEjercicio from './components/DictadoEjercicio';
import ResultadosView from './components/ResultadosView';
import ComprensionEjercicio from './components/ComprensionEjercicio';
import './App.css'

const Home = () => {
  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Typography variant="h3" gutterBottom align="center">
        Evaluación de Dislexia
      </Typography>
      
      <Typography variant="h5" gutterBottom align="center" color="text.secondary" sx={{ mb: 4 }}>
        Plataforma de evaluación interactiva para adultos hispanohablantes
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Card elevation={3}>
            <CardContent>
              <Typography variant="h5" gutterBottom>
                Ejercicio de Lectura
              </Typography>
              <Typography variant="body1" color="text.secondary">
                Evalúa tu capacidad de lectura en voz alta. Este ejercicio analiza tu fluidez, 
                precisión y comprensión lectora.
              </Typography>
            </CardContent>
            <CardActions>
              <Button 
                component={Link} 
                to="/lectura" 
                variant="contained" 
                fullWidth
              >
                Comenzar Ejercicio de Lectura
              </Button>
            </CardActions>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card elevation={3}>
            <CardContent>
              <Typography variant="h5" gutterBottom>
                Ejercicio de Dictado
              </Typography>
              <Typography variant="body1" color="text.secondary">
                Pon a prueba tu capacidad de comprensión auditiva y escritura. 
                Este ejercicio evalúa tu habilidad para transcribir texto hablado.
              </Typography>
            </CardContent>
            <CardActions>
              <Button 
                component={Link} 
                to="/dictado" 
                variant="contained" 
                fullWidth
              >
                Comenzar Ejercicio de Dictado
              </Button>
            </CardActions>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card elevation={3}>
            <CardContent>
              <Typography variant="h5" gutterBottom>
                Comprensión Lectora
              </Typography>
              <Typography variant="body1" color="text.secondary">
                Lee un texto y responde preguntas para evaluar tu comprensión y retención de información.
              </Typography>
            </CardContent>
            <CardActions>
              <Button 
                component={Link} 
                to="/comprension" 
                variant="contained" 
                fullWidth
              >
                Comenzar Ejercicio de Comprensión
              </Button>
            </CardActions>
          </Card>
        </Grid>
      </Grid>

      <Paper elevation={3} sx={{ mt: 4, p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Acerca de la Evaluación
        </Typography>
        <Typography variant="body1" paragraph>
          Esta plataforma utiliza tecnología avanzada de Machine Learning para evaluar 
          patrones cognitivos y lingüísticos asociados con la dislexia en adultos 
          hispanohablantes. Los ejercicios están diseñados para proporcionar una 
          evaluación completa y personalizada.
        </Typography>
        <Typography variant="body1">
          Los resultados incluyen análisis detallados y recomendaciones específicas 
          basadas en el desempeño individual.
        </Typography>
      </Paper>
    </Container>
  );
};

const App = () => {
  return (
    <Router>
      <Box sx={{ flexGrow: 1 }}>
        <AppBar position="static">
          <Toolbar>
            <Typography 
              variant="h6" 
              component={Link} 
              to="/" 
              sx={{ 
                flexGrow: 1, 
                textDecoration: 'none', 
                color: 'inherit' 
              }}
            >
              DislexIA
            </Typography>
          </Toolbar>
        </AppBar>

        <Box sx={{ py: 4 }}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/lectura" element={<LecturaEjercicio />} />
            <Route path="/dictado" element={<DictadoEjercicio />} />
            <Route path="/comprension" element={<ComprensionEjercicio />} />
            <Route path="/resultados" element={<ResultadosView />} />
          </Routes>
        </Box>
      </Box>
    </Router>
  );
};

export default App; 