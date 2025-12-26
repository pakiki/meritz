import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Paper,
  Typography,
  Button,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';
import SaveIcon from '@mui/icons-material/Save';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';

import WorkflowEditor from '../components/WorkflowEditor';
import { getWorkflow, createWorkflow, updateWorkflow } from '../services/api';

const WorkflowPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [workflow, setWorkflow] = useState(null);
  const [openDialog, setOpenDialog] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    version: '1.0.0',
  });

  useEffect(() => {
    if (id) {
      loadWorkflow();
    } else {
      setOpenDialog(true);
    }
  }, [id]);

  const loadWorkflow = async () => {
    try {
      const response = await getWorkflow(id);
      if (response.success) {
        setWorkflow(response.data);
        setFormData({
          name: response.data.name,
          description: response.data.description || '',
          version: response.data.version,
        });
      }
    } catch (error) {
      console.error('Failed to load workflow:', error);
    }
  };

  const handleSave = async (nodes, edges) => {
    try {
      const data = {
        ...formData,
        nodes,
        edges,
      };

      if (id) {
        await updateWorkflow(id, data);
      } else {
        await createWorkflow(data);
      }

      navigate('/dashboard');
    } catch (error) {
      console.error('Failed to save workflow:', error);
    }
  };

  const handleCreateWorkflow = async () => {
    if (!formData.name) {
      alert('워크플로우 이름을 입력하세요.');
      return;
    }

    try {
      const response = await createWorkflow(formData);
      if (response.success) {
        setWorkflow(response.data);
        setOpenDialog(false);
      }
    } catch (error) {
      console.error('Failed to create workflow:', error);
    }
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <Button
            startIcon={<ArrowBackIcon />}
            onClick={() => navigate('/dashboard')}
            sx={{ mr: 2 }}
          >
            돌아가기
          </Button>
          <Typography variant="h4" component="h1">
            {id ? '워크플로우 편집' : '새 워크플로우'}
          </Typography>
        </Box>
        <Button
          variant="contained"
          startIcon={<SaveIcon />}
          onClick={() => handleSave(workflow?.nodes, workflow?.edges)}
        >
          저장
        </Button>
      </Box>

      {workflow && (
        <Paper sx={{ p: 2, mb: 2 }}>
          <Typography variant="h6">{workflow.name}</Typography>
          <Typography variant="body2" color="text.secondary">
            {workflow.description}
          </Typography>
        </Paper>
      )}

      <WorkflowEditor workflow={workflow} onSave={handleSave} />

      <Dialog open={openDialog} onClose={() => {}} maxWidth="sm" fullWidth>
        <DialogTitle>새 워크플로우 생성</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label="워크플로우 이름"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            margin="normal"
            required
          />
          <TextField
            fullWidth
            label="설명"
            value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            margin="normal"
            multiline
            rows={3}
          />
          <TextField
            fullWidth
            label="버전"
            value={formData.version}
            onChange={(e) => setFormData({ ...formData, version: e.target.value })}
            margin="normal"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => navigate('/dashboard')}>취소</Button>
          <Button onClick={handleCreateWorkflow} variant="contained">
            생성
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default WorkflowPage;
