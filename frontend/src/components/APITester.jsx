import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  TextField,
  Button,
  Grid,
  Paper,
  Alert,
  Chip,
  Tabs,
  Tab
} from '@mui/material';
import { PlayArrow, Code, Description } from '@mui/icons-material';
import axios from 'axios';

const APITester = ({ deploymentId }) => {
  const [deployment, setDeployment] = useState(null);
  const [inputJson, setInputJson] = useState('{}');
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [tab, setTab] = useState(0);
  const [swaggerSpec, setSwaggerSpec] = useState(null);

  useEffect(() => {
    if (deploymentId) {
      loadDeployment();
      loadSwagger();
    }
  }, [deploymentId]);

  const loadDeployment = async () => {
    try {
      const response = await axios.get(`http://localhost:5000/api/deployment/${deploymentId}`);
      setDeployment(response.data);
      
      const exampleInput = generateExampleInput(response.data.input_schema);
      setInputJson(JSON.stringify(exampleInput, null, 2));
    } catch (error) {
      console.error('Failed to load deployment:', error);
    }
  };

  const loadSwagger = async () => {
    try {
      const response = await axios.get(`http://localhost:5000/api/deployment/${deploymentId}/swagger`);
      setSwaggerSpec(response.data);
    } catch (error) {
      console.error('Failed to load swagger spec:', error);
    }
  };

  const generateExampleInput = (schema) => {
    const example = {};
    if (schema && schema.properties) {
      Object.keys(schema.properties).forEach((key) => {
        const prop = schema.properties[key];
        if (prop.type === 'number' || prop.type === 'integer') {
          example[key] = 100;
        } else if (prop.type === 'string') {
          example[key] = 'example_value';
        } else if (prop.type === 'boolean') {
          example[key] = true;
        } else {
          example[key] = null;
        }
      });
    }
    return example;
  };

  const handleExecute = async () => {
    setLoading(true);
    setError(null);
    setResponse(null);

    try {
      const inputData = JSON.parse(inputJson);
      const result = await axios.post(
        `http://localhost:5000/api/deployment/${deploymentId}/test`,
        { input: inputData }
      );
      setResponse(result.data);
    } catch (err) {
      setError(err.response?.data?.error || err.message);
    } finally {
      setLoading(false);
    }
  };

  if (!deployment) return <Typography>Loading...</Typography>;

  return (
    <Box sx={{ p: 3 }}>
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Typography variant="h5">{deployment.api_name}</Typography>
            <Chip
              label={deployment.status}
              color={deployment.status === 'active' ? 'success' : 'default'}
            />
          </Box>
          <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
            {deployment.description}
          </Typography>
          <Box sx={{ mt: 2 }}>
            <Typography variant="body2">
              <strong>Path:</strong> {deployment.api_path}
            </Typography>
            <Typography variant="body2">
              <strong>Version:</strong> {deployment.version}
            </Typography>
            <Typography variant="body2">
              <strong>Executions:</strong> {deployment.execution_count}
            </Typography>
          </Box>
        </CardContent>
      </Card>

      <Tabs value={tab} onChange={(e, newValue) => setTab(newValue)} sx={{ mb: 2 }}>
        <Tab label="Test Console" icon={<PlayArrow />} />
        <Tab label="API Documentation" icon={<Description />} />
        <Tab label="Example Code" icon={<Code />} />
      </Tabs>

      {tab === 0 && (
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                Request
              </Typography>
              <TextField
                fullWidth
                multiline
                rows={15}
                value={inputJson}
                onChange={(e) => setInputJson(e.target.value)}
                variant="outlined"
                placeholder="Enter JSON input"
                sx={{ fontFamily: 'monospace', mb: 2 }}
              />
              <Button
                fullWidth
                variant="contained"
                startIcon={<PlayArrow />}
                onClick={handleExecute}
                disabled={loading}
              >
                {loading ? 'Executing...' : 'Execute API'}
              </Button>
            </Paper>
          </Grid>

          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                Response
              </Typography>
              {error && (
                <Alert severity="error" sx={{ mb: 2 }}>
                  {error}
                </Alert>
              )}
              {response && (
                <Box>
                  <Alert severity="success" sx={{ mb: 2 }}>
                    Execution successful
                  </Alert>
                  <TextField
                    fullWidth
                    multiline
                    rows={13}
                    value={JSON.stringify(response, null, 2)}
                    variant="outlined"
                    InputProps={{ readOnly: true }}
                    sx={{ fontFamily: 'monospace' }}
                  />
                </Box>
              )}
              {!response && !error && (
                <Typography color="textSecondary" align="center" sx={{ mt: 5 }}>
                  Execute the API to see the response
                </Typography>
              )}
            </Paper>
          </Grid>
        </Grid>
      )}

      {tab === 1 && swaggerSpec && (
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>
            {swaggerSpec.info.title}
          </Typography>
          <Typography variant="body2" paragraph>
            {swaggerSpec.info.description}
          </Typography>
          
          {Object.entries(swaggerSpec.paths).map(([path, methods]) => (
            <Box key={path} sx={{ mb: 3 }}>
              <Typography variant="subtitle1" sx={{ fontFamily: 'monospace', mb: 1 }}>
                {path}
              </Typography>
              {Object.entries(methods).map(([method, details]) => (
                <Paper key={method} variant="outlined" sx={{ p: 2, mb: 2 }}>
                  <Chip label={method.toUpperCase()} color="primary" size="small" sx={{ mb: 1 }} />
                  <Typography variant="body1" gutterBottom>
                    {details.summary}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    {details.description}
                  </Typography>
                </Paper>
              ))}
            </Box>
          ))}
        </Paper>
      )}

      {tab === 2 && (
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>
            Example Code
          </Typography>
          
          <Typography variant="subtitle2" sx={{ mt: 2, mb: 1 }}>
            cURL
          </Typography>
          <TextField
            fullWidth
            multiline
            rows={5}
            value={`curl -X POST http://localhost:5000${deployment.api_path} \\
  -H "Content-Type: application/json" \\
  -d '${inputJson}'`}
            variant="outlined"
            InputProps={{ readOnly: true }}
            sx={{ fontFamily: 'monospace', mb: 3 }}
          />

          <Typography variant="subtitle2" sx={{ mb: 1 }}>
            Python
          </Typography>
          <TextField
            fullWidth
            multiline
            rows={8}
            value={`import requests

url = "http://localhost:5000${deployment.api_path}"
headers = {"Content-Type": "application/json"}
data = ${inputJson}

response = requests.post(url, json=data, headers=headers)
print(response.json())`}
            variant="outlined"
            InputProps={{ readOnly: true }}
            sx={{ fontFamily: 'monospace', mb: 3 }}
          />

          <Typography variant="subtitle2" sx={{ mb: 1 }}>
            JavaScript
          </Typography>
          <TextField
            fullWidth
            multiline
            rows={10}
            value={`fetch('http://localhost:5000${deployment.api_path}', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(${inputJson})
})
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));`}
            variant="outlined"
            InputProps={{ readOnly: true }}
            sx={{ fontFamily: 'monospace' }}
          />
        </Paper>
      )}
    </Box>
  );
};

export default APITester;
