import React from 'react';
import { Card, CardContent, Typography, CardActionArea } from '@mui/material';

const ExerciseCard = ({ title, description, onClick }) => {
    return (
        <Card sx={{ minWidth: 275, maxWidth: 345, m: 2 }}>
            <CardActionArea onClick={onClick}>
                <CardContent>
                    <Typography variant="h5" component="div" gutterBottom>
                        {title}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                        {description}
                    </Typography>
                </CardContent>
            </CardActionArea>
        </Card>
    );
};

export default ExerciseCard; 