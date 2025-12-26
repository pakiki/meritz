import React from 'react';
import { Box, Paper, Typography, List, ListItem, ListItemButton, ListItemText } from '@mui/material';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import StopIcon from '@mui/icons-material/Stop';
import CallSplitIcon from '@mui/icons-material/CallSplit';
import ScoreIcon from '@mui/icons-material/Score';
import ApiIcon from '@mui/icons-material/Api';

const nodeTypes = [
  { type: 'start', label: '시작', icon: <PlayArrowIcon /> },
  { type: 'end', label: '종료', icon: <StopIcon /> },
  { type: 'decision', label: '의사결정', icon: <CallSplitIcon /> },
  { type: 'score', label: '점수 계산', icon: <ScoreIcon /> },
  { type: 'api', label: 'API 호출', icon: <ApiIcon /> },
];

const NodePalette = () => {
  const onDragStart = (event, nodeType) => {
    event.dataTransfer.setData('application/reactflow', nodeType);
    event.dataTransfer.effectAllowed = 'move';
  };

  return (
    <Paper sx={{ width: 250, mr: 2, p: 2 }}>
      <Typography variant="h6" gutterBottom>
        노드 팔레트
      </Typography>
      <Typography variant="caption" color="text.secondary" paragraph>
        노드를 드래그하여 캔버스에 추가하세요
      </Typography>
      
      <List>
        {nodeTypes.map((node) => (
          <ListItem key={node.type} disablePadding>
            <ListItemButton
              draggable
              onDragStart={(event) => onDragStart(event, node.type)}
              sx={{
                border: '1px solid',
                borderColor: 'divider',
                borderRadius: 1,
                mb: 1,
                cursor: 'grab',
                '&:active': {
                  cursor: 'grabbing',
                },
              }}
            >
              <Box sx={{ mr: 1, display: 'flex', alignItems: 'center' }}>
                {node.icon}
              </Box>
              <ListItemText primary={node.label} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </Paper>
  );
};

export default NodePalette;
