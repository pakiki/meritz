import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  List,
  ListItem,
  ListItemText,
  Chip,
} from '@mui/material';
import { getApplicationLogs } from '../services/api';

const ExecutionMonitor = ({ applicationId }) => {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (applicationId) {
      loadLogs();
    }
  }, [applicationId]);

  const loadLogs = async () => {
    setLoading(true);
    try {
      const response = await getApplicationLogs(applicationId);
      if (response.success) {
        setLogs(response.data);
      }
    } catch (error) {
      console.error('Failed to load logs:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'success':
        return 'success';
      case 'error':
        return 'error';
      case 'processing':
        return 'warning';
      default:
        return 'default';
    }
  };

  return (
    <Paper sx={{ p: 2, height: '100%', overflow: 'auto' }}>
      <Typography variant="h6" gutterBottom>
        실행 모니터
      </Typography>

      {loading ? (
        <Typography>로딩 중...</Typography>
      ) : logs.length === 0 ? (
        <Typography color="text.secondary">
          실행 로그가 없습니다
        </Typography>
      ) : (
        <List>
          {logs.map((log) => (
            <ListItem key={log.id} divider>
              <ListItemText
                primary={
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Typography variant="body2">
                      {log.node_type} - {log.action}
                    </Typography>
                    <Chip
                      label={log.status}
                      color={getStatusColor(log.status)}
                      size="small"
                    />
                  </Box>
                }
                secondary={
                  <Box>
                    {log.error_message && (
                      <Typography variant="caption" color="error">
                        {log.error_message}
                      </Typography>
                    )}
                    <Typography variant="caption" color="text.secondary">
                      {new Date(log.created_at).toLocaleString()}
                      {log.execution_time && ` - ${log.execution_time.toFixed(3)}초`}
                    </Typography>
                  </Box>
                }
              />
            </ListItem>
          ))}
        </List>
      )}
    </Paper>
  );
};

export default ExecutionMonitor;
