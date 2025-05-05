import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Box, AppBar, Toolbar, Typography } from '@mui/material';
import Inicio from './components/Inicio';
import TestFlow from './components/TestFlow';
import ResultadosView from './components/ResultadosView';
import './App.css';

const App = () => {
  return (
    <Router>
      <Box sx={{ flexGrow: 1 }}>
        <AppBar position="static">
          <Toolbar>
            <Typography 
              variant="h6" 
              component="div"
              sx={{ flexGrow: 1, textDecoration: 'none', color: 'inherit' }}
            >
              DislexIA
            </Typography>
          </Toolbar>
        </AppBar>
        <Box sx={{ py: 4 }}>
          <Routes>
            <Route path="/" element={<Inicio />} />
            <Route path="/test" element={<TestFlow />} />
            <Route path="/resultados" element={<ResultadosView />} />
          </Routes>
        </Box>
      </Box>
    </Router>
  );
};

export default App; 