import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  TextField,
  Divider,
} from '@mui/material';

const PropertyPanel = ({ node, onChange }) => {
  const [label, setLabel] = useState(node?.data?.label || '');

  const handleLabelChange = (event) => {
    const newLabel = event.target.value;
    setLabel(newLabel);
    onChange({ label: newLabel });
  };

  if (!node) {
    return null;
  }

  return (
    <Paper sx={{ width: 300, ml: 2, p: 2 }}>
      <Typography variant="h6" gutterBottom>
        속성 패널
      </Typography>
      
      <Divider sx={{ my: 2 }} />
      
      <Box sx={{ mb: 2 }}>
        <Typography variant="caption" color="text.secondary">
          노드 ID
        </Typography>
        <Typography variant="body2">{node.id}</Typography>
      </Box>

      <Box sx={{ mb: 2 }}>
        <Typography variant="caption" color="text.secondary">
          노드 타입
        </Typography>
        <Typography variant="body2">{node.type}</Typography>
      </Box>

      <TextField
        fullWidth
        label="레이블"
        value={label}
        onChange={handleLabelChange}
        size="small"
        sx={{ mb: 2 }}
      />

      <Box sx={{ mb: 2 }}>
        <Typography variant="caption" color="text.secondary">
          위치
        </Typography>
        <Typography variant="body2">
          X: {Math.round(node.position.x)}, Y: {Math.round(node.position.y)}
        </Typography>
      </Box>
    </Paper>
  );
};

export default PropertyPanel;
