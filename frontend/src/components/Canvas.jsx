import React from 'react';
import { Box, Paper } from '@mui/material';

const Canvas = ({ children }) => {
  return (
    <Paper
      sx={{
        flex: 1,
        position: 'relative',
        overflow: 'hidden',
        backgroundColor: '#fafafa',
      }}
    >
      <Box
        sx={{
          width: '100%',
          height: '100%',
          position: 'relative',
        }}
      >
        {children}
      </Box>
    </Paper>
  );
};

export default Canvas;
