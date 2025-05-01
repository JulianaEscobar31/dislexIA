import React from 'react';
import { 
    Paper, 
    Typography, 
    Box, 
    LinearProgress,
    List,
    ListItem,
    ListItemIcon,
    ListItemText
} from '@mui/material';
import InfoIcon from '@mui/icons-material/Info';

const ResultsView = ({ resultado }) => {
    if (!resultado) return null;

    return (
        <Paper elevation={3} sx={{ p: 4, mt: 4 }}>
            <Typography variant="h5" gutterBottom>
                Resultados del Análisis
            </Typography>

            <Box sx={{ mb: 3 }}>
                <Typography variant="subtitle1" color="primary" gutterBottom>
                    Puntuación General: {resultado.puntuacion_general.toFixed(1)}%
                </Typography>
                <LinearProgress 
                    variant="determinate" 
                    value={resultado.puntuacion_general} 
                    sx={{ height: 10, borderRadius: 5 }}
                />
            </Box>

            <Typography variant="h6" gutterBottom>
                Métricas Detalladas
            </Typography>
            
            <Box sx={{ mb: 3 }}>
                <Typography paragraph>
                    <strong>Duración:</strong> {resultado.duracion.toFixed(2)} segundos
                </Typography>
                <Typography paragraph>
                    <strong>Palabras por minuto:</strong> {resultado.palabras_por_minuto.toFixed(2)}
                </Typography>
                <Typography paragraph>
                    <strong>Precisión:</strong> {resultado.precision_lectura.toFixed(1)}%
                </Typography>
            </Box>

            <Typography variant="h6" gutterBottom>
                Errores Detectados
            </Typography>
            <Box sx={{ mb: 3 }}>
                {Object.entries(resultado.errores_detectados).map(([tipo, cantidad]) => (
                    <Typography key={tipo} paragraph>
                        <strong>{tipo.charAt(0).toUpperCase() + tipo.slice(1)}:</strong> {cantidad}
                    </Typography>
                ))}
            </Box>

            {resultado.recomendaciones && resultado.recomendaciones.length > 0 && (
                <>
                    <Typography variant="h6" gutterBottom>
                        Recomendaciones
                    </Typography>
                    <List>
                        {resultado.recomendaciones.filter(Boolean).map((recomendacion, index) => (
                            <ListItem key={index}>
                                <ListItemIcon>
                                    <InfoIcon color="primary" />
                                </ListItemIcon>
                                <ListItemText primary={recomendacion} />
                            </ListItem>
                        ))}
                    </List>
                </>
            )}
        </Paper>
    );
};

export default ResultsView; 