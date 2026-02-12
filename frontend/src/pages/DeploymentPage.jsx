import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Typography,
  Button,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Paper,
  Chip,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Select,
  MenuItem,
  FormControl,
  InputLabel
} from '@mui/material';
import { Visibility, Delete, Refresh, Add } from '@mui/icons-material';
import axios from 'axios';
import APITester from '../components/APITester';

const DeploymentPage = () => {
  const [deployments, setDeployments] = useState([]);
  const [workflows, setWorkflows] = useState([]);
  const [selectedDeployment, setSelectedDeployment] = useState(null);
  const [openTestDialog, setOpenTestDialog] = useState(false);
  const [openDeployDialog, setOpenDeployDialog] = useState(false);
  const [selectedWorkflow, setSelectedWorkflow] = useState('');

  useEffect(() => {
    loadDeployments();
    loadWorkflows();
  }, []);

  const loadDeployments = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/deployment');
      setDeployments(response.data);
    } catch (error) {
      console.error('Failed to load deployments:', error);
    }
  };

  const loadWorkflows = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/workflow');
      setWorkflows(response.data);
    } catch (error) {
      console.error('Failed to load workflows:', error);
    }
  };

  const handleDeploy = async () => {
    try {
      await axios.post(`http://localhost:5000/api/deployment/workflow/${selectedWorkflow}`);
      loadDeployments();
      setOpenDeployDialog(false);
      setSelectedWorkflow('');
    } catch (error) {
      console.error('Failed to deploy workflow:', error);
      alert(error.response?.data?.error || 'Failed to deploy workflow');
    }
  };

  const handleUndeploy = async (deploymentId) => {
    if (!window.confirm('Are you sure you want to undeploy this API?')) return;
    
    try {
      await axios.delete(`http://localhost:5000/api/deployment/${deploymentId}`);
      loadDeployments();
    } catch (error) {
      console.error('Failed to undeploy API:', error);
    }
  };

  const handleRedeploy = async (deploymentId) => {
    try {
      await axios.post(`http://localhost:5000/api/deployment/${deploymentId}/redeploy`);
      loadDeployments();
    } catch (error) {
      console.error('Failed to redeploy API:', error);
    }
  };

  const handleTest = (deployment) => {
    setSelectedDeployment(deployment);
    setOpenTestDialog(true);
  };

  return (
    <Container maxWidth="xl">
      <Box sx={{ my: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
          <Typography variant="h4">API Deployments</Typography>
          <Button
            variant="contained"
            startIcon={<Add />}
            onClick={() => setOpenDeployDialog(true)}
          >
            Deploy Workflow
          </Button>
        </Box>

        <Paper>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>API Name</TableCell>
                <TableCell>Path</TableCell>
                <TableCell>Version</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Executions</TableCell>
                <TableCell>Last Executed</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {deployments.map((deployment) => (
                <TableRow key={deployment.id}>
                  <TableCell>{deployment.api_name}</TableCell>
                  <TableCell>
                    <code>{deployment.api_path}</code>
                  </TableCell>
                  <TableCell>{deployment.version}</TableCell>
                  <TableCell>
                    <Chip
                      label={deployment.status}
                      color={deployment.status === 'active' ? 'success' : 'default'}
                      size="small"
                    />
                  </TableCell>
                  <TableCell>{deployment.execution_count}</TableCell>
                  <TableCell>
                    {deployment.last_executed_at
                      ? new Date(deployment.last_executed_at).toLocaleString()
                      : '-'}
                  </TableCell>
                  <TableCell>
                    <IconButton
                      size="small"
                      onClick={() => handleTest(deployment)}
                      title="Test API"
                    >
                      <Visibility />
                    </IconButton>
                    <IconButton
                      size="small"
                      onClick={() => handleRedeploy(deployment.id)}
                      title="Redeploy"
                    >
                      <Refresh />
                    </IconButton>
                    <IconButton
                      size="small"
                      onClick={() => handleUndeploy(deployment.id)}
                      title="Undeploy"
                    >
                      <Delete />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))}
              {deployments.length === 0 && (
                <TableRow>
                  <TableCell colSpan={7} align="center">
                    <Typography color="textSecondary">
                      No deployments found. Deploy a workflow to get started.
                    </Typography>
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </Paper>
      </Box>

      <Dialog
        open={openDeployDialog}
        onClose={() => setOpenDeployDialog(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Deploy Workflow as API</DialogTitle>
        <DialogContent>
          <FormControl fullWidth sx={{ mt: 2 }}>
            <InputLabel>Select Workflow</InputLabel>
            <Select
              value={selectedWorkflow}
              onChange={(e) => setSelectedWorkflow(e.target.value)}
              label="Select Workflow"
            >
              {workflows.map((workflow) => (
                <MenuItem key={workflow.id} value={workflow.id}>
                  {workflow.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDeployDialog(false)}>Cancel</Button>
          <Button
            onClick={handleDeploy}
            variant="contained"
            disabled={!selectedWorkflow}
          >
            Deploy
          </Button>
        </DialogActions>
      </Dialog>

      <Dialog
        open={openTestDialog}
        onClose={() => setOpenTestDialog(false)}
        maxWidth="xl"
        fullWidth
      >
        <DialogTitle>Test API</DialogTitle>
        <DialogContent>
          {selectedDeployment && (
            <APITester deploymentId={selectedDeployment.id} />
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenTestDialog(false)}>Close</Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default DeploymentPage;
