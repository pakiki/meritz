import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  TextField,
  Button,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Grid,
  Chip
} from '@mui/material';
import { Add, Delete, Calculate } from '@mui/icons-material';
import axios from 'axios';

const ScorecardDesigner = ({ scorecardId }) => {
  const [scorecard, setScorecard] = useState(null);
  const [characteristics, setCharacteristics] = useState([]);
  const [openCharDialog, setOpenCharDialog] = useState(false);
  const [openAttrDialog, setOpenAttrDialog] = useState(false);
  const [selectedChar, setSelectedChar] = useState(null);
  const [testInput, setTestInput] = useState({});
  const [testResult, setTestResult] = useState(null);

  const [newChar, setNewChar] = useState({ name: '', weight: 0 });
  const [newAttr, setNewAttr] = useState({
    attribute: '',
    min_value: '',
    max_value: '',
    good_count: 0,
    bad_count: 0
  });

  useEffect(() => {
    if (scorecardId) {
      loadScorecard();
    }
  }, [scorecardId]);

  const loadScorecard = async () => {
    try {
      const response = await axios.get(`http://localhost:5000/api/scorecard/${scorecardId}`);
      setScorecard(response.data);
      setCharacteristics(response.data.characteristics || []);
    } catch (error) {
      console.error('Failed to load scorecard:', error);
    }
  };

  const handleAddCharacteristic = async () => {
    try {
      await axios.post(
        `http://localhost:5000/api/scorecard/${scorecardId}/characteristic`,
        newChar
      );
      loadScorecard();
      setOpenCharDialog(false);
      setNewChar({ name: '', weight: 0 });
    } catch (error) {
      console.error('Failed to add characteristic:', error);
    }
  };

  const handleAddAttribute = async () => {
    try {
      await axios.post(
        `http://localhost:5000/api/scorecard/characteristic/${selectedChar.id}/attribute`,
        {
          ...newAttr,
          total_good: 100,
          total_bad: 100
        }
      );
      loadScorecard();
      setOpenAttrDialog(false);
      setNewAttr({ attribute: '', min_value: '', max_value: '', good_count: 0, bad_count: 0 });
    } catch (error) {
      console.error('Failed to add attribute:', error);
    }
  };

  const handleCalculateScore = async () => {
    try {
      const response = await axios.post(
        `http://localhost:5000/api/scorecard/${scorecardId}/calculate`,
        { input: testInput }
      );
      setTestResult(response.data);
    } catch (error) {
      console.error('Failed to calculate score:', error);
    }
  };

  if (!scorecard) return <Typography>Loading...</Typography>;

  return (
    <Box sx={{ p: 3 }}>
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h5" gutterBottom>
            {scorecard.name}
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={4}>
              <Typography variant="body2" color="textSecondary">
                Base Score: {scorecard.base_score}
              </Typography>
            </Grid>
            <Grid item xs={4}>
              <Typography variant="body2" color="textSecondary">
                PDO: {scorecard.pdo}
              </Typography>
            </Grid>
            <Grid item xs={4}>
              <Typography variant="body2" color="textSecondary">
                Base Odds: {scorecard.base_odds}
              </Typography>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
            <Typography variant="h6">Characteristics</Typography>
            <Button
              startIcon={<Add />}
              variant="contained"
              onClick={() => setOpenCharDialog(true)}
            >
              Add Characteristic
            </Button>
          </Box>

          {characteristics.map((char) => (
            <Box key={char.id} sx={{ mb: 3 }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                <Typography variant="subtitle1">
                  {char.name} <Chip label={`${char.weight}%`} size="small" />
                </Typography>
                <Button
                  size="small"
                  startIcon={<Add />}
                  onClick={() => {
                    setSelectedChar(char);
                    setOpenAttrDialog(true);
                  }}
                >
                  Add Attribute
                </Button>
              </Box>
              
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>Attribute</TableCell>
                    <TableCell>Range</TableCell>
                    <TableCell>Good</TableCell>
                    <TableCell>Bad</TableCell>
                    <TableCell>WOE</TableCell>
                    <TableCell>IV</TableCell>
                    <TableCell>Points</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {(char.attributes || []).map((attr) => (
                    <TableRow key={attr.id}>
                      <TableCell>{attr.attribute}</TableCell>
                      <TableCell>
                        {attr.min_value !== null && attr.max_value !== null
                          ? `${attr.min_value} - ${attr.max_value}`
                          : attr.category || '-'}
                      </TableCell>
                      <TableCell>{attr.good_count}</TableCell>
                      <TableCell>{attr.bad_count}</TableCell>
                      <TableCell>{attr.woe?.toFixed(4) || '-'}</TableCell>
                      <TableCell>{attr.iv?.toFixed(4) || '-'}</TableCell>
                      <TableCell>{attr.points?.toFixed(2) || '-'}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </Box>
          ))}
        </CardContent>
      </Card>

      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Test Scorecard
          </Typography>
          <Grid container spacing={2}>
            {characteristics.map((char) => (
              <Grid item xs={6} key={char.id}>
                <TextField
                  fullWidth
                  label={char.name}
                  type="number"
                  value={testInput[char.name] || ''}
                  onChange={(e) => setTestInput({
                    ...testInput,
                    [char.name]: parseFloat(e.target.value)
                  })}
                />
              </Grid>
            ))}
          </Grid>
          <Button
            sx={{ mt: 2 }}
            variant="contained"
            startIcon={<Calculate />}
            onClick={handleCalculateScore}
          >
            Calculate Score
          </Button>

          {testResult && (
            <Box sx={{ mt: 3 }}>
              <Typography variant="h6">
                Total Score: {testResult.score}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Probability: {(testResult.probability * 100).toFixed(2)}%
              </Typography>
              <Table size="small" sx={{ mt: 2 }}>
                <TableHead>
                  <TableRow>
                    <TableCell>Characteristic</TableCell>
                    <TableCell>Value</TableCell>
                    <TableCell>Attribute</TableCell>
                    <TableCell>Points</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {testResult.breakdown.map((item, idx) => (
                    <TableRow key={idx}>
                      <TableCell>{item.characteristic}</TableCell>
                      <TableCell>{item.value}</TableCell>
                      <TableCell>{item.attribute}</TableCell>
                      <TableCell>{item.points.toFixed(2)}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </Box>
          )}
        </CardContent>
      </Card>

      <Dialog open={openCharDialog} onClose={() => setOpenCharDialog(false)}>
        <DialogTitle>Add Characteristic</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label="Name"
            value={newChar.name}
            onChange={(e) => setNewChar({ ...newChar, name: e.target.value })}
            sx={{ mt: 2, mb: 2 }}
          />
          <TextField
            fullWidth
            label="Weight (%)"
            type="number"
            value={newChar.weight}
            onChange={(e) => setNewChar({ ...newChar, weight: parseFloat(e.target.value) })}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenCharDialog(false)}>Cancel</Button>
          <Button onClick={handleAddCharacteristic} variant="contained">
            Add
          </Button>
        </DialogActions>
      </Dialog>

      <Dialog open={openAttrDialog} onClose={() => setOpenAttrDialog(false)}>
        <DialogTitle>Add Attribute</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label="Attribute Name"
            value={newAttr.attribute}
            onChange={(e) => setNewAttr({ ...newAttr, attribute: e.target.value })}
            sx={{ mt: 2, mb: 2 }}
          />
          <TextField
            fullWidth
            label="Min Value"
            type="number"
            value={newAttr.min_value}
            onChange={(e) => setNewAttr({ ...newAttr, min_value: parseFloat(e.target.value) })}
            sx={{ mb: 2 }}
          />
          <TextField
            fullWidth
            label="Max Value"
            type="number"
            value={newAttr.max_value}
            onChange={(e) => setNewAttr({ ...newAttr, max_value: parseFloat(e.target.value) })}
            sx={{ mb: 2 }}
          />
          <TextField
            fullWidth
            label="Good Count"
            type="number"
            value={newAttr.good_count}
            onChange={(e) => setNewAttr({ ...newAttr, good_count: parseInt(e.target.value) })}
            sx={{ mb: 2 }}
          />
          <TextField
            fullWidth
            label="Bad Count"
            type="number"
            value={newAttr.bad_count}
            onChange={(e) => setNewAttr({ ...newAttr, bad_count: parseInt(e.target.value) })}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenAttrDialog(false)}>Cancel</Button>
          <Button onClick={handleAddAttribute} variant="contained">
            Add
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default ScorecardDesigner;
