import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Paper,
  Typography,
  Button,
  TextField,
  Grid,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Divider,
} from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';

import ExecutionMonitor from '../components/ExecutionMonitor';
import {
  getApplication,
  createApplication,
  executeApplication,
  getWorkflows,
} from '../services/api';

const ApplicationPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [application, setApplication] = useState(null);
  const [workflows, setWorkflows] = useState([]);
  const [formData, setFormData] = useState({
    workflow_id: '',
    applicant_name: '',
    applicant_id: '',
    income: '',
    credit_history: '',
    debt_ratio: '',
    employment_years: '',
  });

  useEffect(() => {
    loadWorkflows();
    if (id) {
      loadApplication();
    }
  }, [id]);

  const loadWorkflows = async () => {
    try {
      const response = await getWorkflows();
      if (response.success) {
        setWorkflows(response.data);
      }
    } catch (error) {
      console.error('Failed to load workflows:', error);
    }
  };

  const loadApplication = async () => {
    try {
      const response = await getApplication(id);
      if (response.success) {
        setApplication(response.data);
        const appData = response.data.application_data;
        setFormData({
          workflow_id: response.data.workflow_id,
          applicant_name: appData.applicant_name || '',
          applicant_id: appData.applicant_id || '',
          income: appData.income || '',
          credit_history: appData.credit_history || '',
          debt_ratio: appData.debt_ratio || '',
          employment_years: appData.employment_years || '',
        });
      }
    } catch (error) {
      console.error('Failed to load application:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const data = {
        workflow_id: formData.workflow_id,
        application_data: {
          applicant_name: formData.applicant_name,
          applicant_id: formData.applicant_id,
          income: parseFloat(formData.income) || 0,
          credit_history: parseInt(formData.credit_history) || 0,
          debt_ratio: parseFloat(formData.debt_ratio) || 0,
          employment_years: parseInt(formData.employment_years) || 0,
        },
      };

      const response = await createApplication(data);
      if (response.success) {
        navigate(`/application/${response.data.id}`);
      }
    } catch (error) {
      console.error('Failed to create application:', error);
    }
  };

  const handleExecute = async () => {
    try {
      const response = await executeApplication(id);
      if (response.success) {
        loadApplication();
      }
    } catch (error) {
      console.error('Failed to execute application:', error);
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
            {id ? '신청서 상세' : '새 신청서'}
          </Typography>
        </Box>
        {id && application?.status === 'pending' && (
          <Button
            variant="contained"
            startIcon={<PlayArrowIcon />}
            onClick={handleExecute}
          >
            실행
          </Button>
        )}
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12} md={id ? 6 : 12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              신청 정보
            </Typography>

            <form onSubmit={handleSubmit}>
              <FormControl fullWidth margin="normal" required>
                <InputLabel>워크플로우</InputLabel>
                <Select
                  value={formData.workflow_id}
                  onChange={(e) => setFormData({ ...formData, workflow_id: e.target.value })}
                  disabled={!!id}
                >
                  {workflows.map((workflow) => (
                    <MenuItem key={workflow.id} value={workflow.id}>
                      {workflow.name}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>

              <TextField
                fullWidth
                label="신청자 이름"
                value={formData.applicant_name}
                onChange={(e) => setFormData({ ...formData, applicant_name: e.target.value })}
                margin="normal"
                required
                disabled={!!id}
              />

              <TextField
                fullWidth
                label="신청자 식별번호"
                value={formData.applicant_id}
                onChange={(e) => setFormData({ ...formData, applicant_id: e.target.value })}
                margin="normal"
                required
                disabled={!!id}
              />

              <Divider sx={{ my: 2 }} />

              <Typography variant="subtitle1" gutterBottom>
                평가 정보
              </Typography>

              <TextField
                fullWidth
                label="연소득 (만원)"
                type="number"
                value={formData.income}
                onChange={(e) => setFormData({ ...formData, income: e.target.value })}
                margin="normal"
                disabled={!!id}
              />

              <TextField
                fullWidth
                label="신용 이력 (개월)"
                type="number"
                value={formData.credit_history}
                onChange={(e) => setFormData({ ...formData, credit_history: e.target.value })}
                margin="normal"
                disabled={!!id}
              />

              <TextField
                fullWidth
                label="부채 비율 (0-1)"
                type="number"
                inputProps={{ step: '0.01', min: '0', max: '1' }}
                value={formData.debt_ratio}
                onChange={(e) => setFormData({ ...formData, debt_ratio: e.target.value })}
                margin="normal"
                disabled={!!id}
              />

              <TextField
                fullWidth
                label="재직 기간 (년)"
                type="number"
                value={formData.employment_years}
                onChange={(e) => setFormData({ ...formData, employment_years: e.target.value })}
                margin="normal"
                disabled={!!id}
              />

              {!id && (
                <Button
                  type="submit"
                  variant="contained"
                  fullWidth
                  sx={{ mt: 3 }}
                >
                  신청서 생성
                </Button>
              )}
            </form>

            {application && (
              <Box sx={{ mt: 3 }}>
                <Divider sx={{ my: 2 }} />
                <Typography variant="subtitle1" gutterBottom>
                  평가 결과
                </Typography>
                <Typography variant="body2">
                  상태: {application.status}
                </Typography>
                {application.score && (
                  <Typography variant="body2">
                    점수: {application.score}
                  </Typography>
                )}
              </Box>
            )}
          </Paper>
        </Grid>

        {id && (
          <Grid item xs={12} md={6}>
            <ExecutionMonitor applicationId={id} />
          </Grid>
        )}
      </Grid>
    </Box>
  );
};

export default ApplicationPage;
