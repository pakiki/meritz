import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Link } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import Button from '@mui/material/Button';

import Dashboard from './pages/Dashboard';
import WorkflowPage from './pages/WorkflowPage';
import ApplicationPage from './pages/ApplicationPage';
import ScorecardPage from './pages/ScorecardPage';
import DeploymentPage from './pages/DeploymentPage';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
          <AppBar position="static">
            <Toolbar>
              <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                Credit Evaluation BPM System
              </Typography>
              <Button color="inherit" component={Link} to="/dashboard">
                Dashboard
              </Button>
              <Button color="inherit" component={Link} to="/workflow">
                Workflows
              </Button>
              <Button color="inherit" component={Link} to="/scorecard">
                Scorecards
              </Button>
              <Button color="inherit" component={Link} to="/deployment">
                Deployments
              </Button>
              <Button color="inherit" component={Link} to="/application">
                Applications
              </Button>
            </Toolbar>
          </AppBar>
          
          <Container maxWidth={false} sx={{ mt: 4, mb: 4, flex: 1 }}>
            <Routes>
              <Route path="/" element={<Navigate to="/dashboard" replace />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/workflow" element={<WorkflowPage />} />
              <Route path="/workflow/:id" element={<WorkflowPage />} />
              <Route path="/scorecard" element={<ScorecardPage />} />
              <Route path="/deployment" element={<DeploymentPage />} />
              <Route path="/application" element={<ApplicationPage />} />
              <Route path="/application/:id" element={<ApplicationPage />} />
            </Routes>
          </Container>
        </Box>
      </Router>
    </ThemeProvider>
  );
}

export default App;
