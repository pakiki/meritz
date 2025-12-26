import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Grid,
  Paper,
  Typography,
  Button,
  Card,
  CardContent,
  CardActions,
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import AccountTreeIcon from '@mui/icons-material/AccountTree';
import AssignmentIcon from '@mui/icons-material/Assignment';

import { getWorkflows, getApplications } from '../services/api';

const Dashboard = () => {
  const navigate = useNavigate();
  const [workflows, setWorkflows] = useState([]);
  const [applications, setApplications] = useState([]);
  const [stats, setStats] = useState({
    totalWorkflows: 0,
    totalApplications: 0,
    pendingApplications: 0,
  });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const workflowsRes = await getWorkflows();
      const applicationsRes = await getApplications();

      if (workflowsRes.success) {
        setWorkflows(workflowsRes.data);
        setStats((prev) => ({ ...prev, totalWorkflows: workflowsRes.data.length }));
      }

      if (applicationsRes.success) {
        setApplications(applicationsRes.data);
        setStats((prev) => ({
          ...prev,
          totalApplications: applicationsRes.data.length,
          pendingApplications: applicationsRes.data.filter((app) => app.status === 'pending').length,
        }));
      }
    } catch (error) {
      console.error('Failed to load data:', error);
    }
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4" component="h1">
          대시보드
        </Typography>
        <Box>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => navigate('/workflow')}
            sx={{ mr: 1 }}
          >
            새 워크플로우
          </Button>
          <Button
            variant="outlined"
            startIcon={<AddIcon />}
            onClick={() => navigate('/application')}
          >
            새 신청서
          </Button>
        </Box>
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, textAlign: 'center' }}>
            <AccountTreeIcon sx={{ fontSize: 48, color: 'primary.main', mb: 1 }} />
            <Typography variant="h3" component="div">
              {stats.totalWorkflows}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              전체 워크플로우
            </Typography>
          </Paper>
        </Grid>

        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, textAlign: 'center' }}>
            <AssignmentIcon sx={{ fontSize: 48, color: 'secondary.main', mb: 1 }} />
            <Typography variant="h3" component="div">
              {stats.totalApplications}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              전체 신청서
            </Typography>
          </Paper>
        </Grid>

        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, textAlign: 'center' }}>
            <AssignmentIcon sx={{ fontSize: 48, color: 'warning.main', mb: 1 }} />
            <Typography variant="h3" component="div">
              {stats.pendingApplications}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              대기 중인 신청서
            </Typography>
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              최근 워크플로우
            </Typography>
            {workflows.slice(0, 5).map((workflow) => (
              <Card key={workflow.id} sx={{ mb: 2 }}>
                <CardContent>
                  <Typography variant="h6">{workflow.name}</Typography>
                  <Typography variant="body2" color="text.secondary">
                    {workflow.description}
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    버전: {workflow.version} | 상태: {workflow.status}
                  </Typography>
                </CardContent>
                <CardActions>
                  <Button size="small" onClick={() => navigate(`/workflow/${workflow.id}`)}>
                    편집
                  </Button>
                </CardActions>
              </Card>
            ))}
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              최근 신청서
            </Typography>
            {applications.slice(0, 5).map((application) => (
              <Card key={application.id} sx={{ mb: 2 }}>
                <CardContent>
                  <Typography variant="h6">{application.applicant_name}</Typography>
                  <Typography variant="body2" color="text.secondary">
                    신청자 ID: {application.applicant_id}
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    상태: {application.status}
                    {application.score && ` | 점수: ${application.score}`}
                  </Typography>
                </CardContent>
                <CardActions>
                  <Button size="small" onClick={() => navigate(`/application/${application.id}`)}>
                    상세보기
                  </Button>
                </CardActions>
              </Card>
            ))}
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
