import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Typography,
  Button,
  List,
  ListItem,
  ListItemText,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Grid,
  Paper
} from '@mui/material';
import { Add } from '@mui/icons-material';
import axios from 'axios';
import ScorecardDesigner from '../components/ScorecardDesigner';

const ScorecardPage = () => {
  const [scorecards, setScorecards] = useState([]);
  const [selectedScorecard, setSelectedScorecard] = useState(null);
  const [openDialog, setOpenDialog] = useState(false);
  const [newScorecard, setNewScorecard] = useState({
    name: '',
    description: '',
    base_score: 600,
    pdo: 20,
    base_odds: 50
  });

  useEffect(() => {
    loadScorecards();
  }, []);

  const loadScorecards = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/scorecard');
      setScorecards(response.data);
      if (response.data.length > 0 && !selectedScorecard) {
        setSelectedScorecard(response.data[0]);
      }
    } catch (error) {
      console.error('Failed to load scorecards:', error);
    }
  };

  const handleCreate = async () => {
    try {
      const response = await axios.post('http://localhost:5000/api/scorecard', newScorecard);
      setScorecards([...scorecards, response.data]);
      setSelectedScorecard(response.data);
      setOpenDialog(false);
      setNewScorecard({
        name: '',
        description: '',
        base_score: 600,
        pdo: 20,
        base_odds: 50
      });
    } catch (error) {
      console.error('Failed to create scorecard:', error);
    }
  };

  return (
    <Container maxWidth="xl">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" gutterBottom>
          Scorecard Designer
        </Typography>
        
        <Grid container spacing={3}>
          <Grid item xs={3}>
            <Paper sx={{ p: 2 }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                <Typography variant="h6">Scorecards</Typography>
                <Button
                  size="small"
                  startIcon={<Add />}
                  onClick={() => setOpenDialog(true)}
                >
                  New
                </Button>
              </Box>
              <List>
                {scorecards.map((scorecard) => (
                  <ListItem
                    key={scorecard.id}
                    button
                    selected={selectedScorecard?.id === scorecard.id}
                    onClick={() => setSelectedScorecard(scorecard)}
                  >
                    <ListItemText
                      primary={scorecard.name}
                      secondary={scorecard.status}
                    />
                  </ListItem>
                ))}
              </List>
            </Paper>
          </Grid>
          
          <Grid item xs={9}>
            {selectedScorecard ? (
              <ScorecardDesigner
                scorecardId={selectedScorecard.id}
                key={selectedScorecard.id}
              />
            ) : (
              <Paper sx={{ p: 5, textAlign: 'center' }}>
                <Typography color="textSecondary">
                  Select a scorecard or create a new one
                </Typography>
              </Paper>
            )}
          </Grid>
        </Grid>
      </Box>

      <Dialog open={openDialog} onClose={() => setOpenDialog(false)}>
        <DialogTitle>Create New Scorecard</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label="Name"
            value={newScorecard.name}
            onChange={(e) => setNewScorecard({ ...newScorecard, name: e.target.value })}
            sx={{ mt: 2, mb: 2 }}
          />
          <TextField
            fullWidth
            label="Description"
            multiline
            rows={3}
            value={newScorecard.description}
            onChange={(e) => setNewScorecard({ ...newScorecard, description: e.target.value })}
            sx={{ mb: 2 }}
          />
          <Grid container spacing={2}>
            <Grid item xs={4}>
              <TextField
                fullWidth
                label="Base Score"
                type="number"
                value={newScorecard.base_score}
                onChange={(e) => setNewScorecard({ ...newScorecard, base_score: parseFloat(e.target.value) })}
              />
            </Grid>
            <Grid item xs={4}>
              <TextField
                fullWidth
                label="PDO"
                type="number"
                value={newScorecard.pdo}
                onChange={(e) => setNewScorecard({ ...newScorecard, pdo: parseFloat(e.target.value) })}
              />
            </Grid>
            <Grid item xs={4}>
              <TextField
                fullWidth
                label="Base Odds"
                type="number"
                value={newScorecard.base_odds}
                onChange={(e) => setNewScorecard({ ...newScorecard, base_odds: parseFloat(e.target.value) })}
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>Cancel</Button>
          <Button onClick={handleCreate} variant="contained">
            Create
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default ScorecardPage;
