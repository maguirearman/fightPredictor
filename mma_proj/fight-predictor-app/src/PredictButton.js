// PredictButton.js
import React from 'react';
import Button from '@mui/material/Button';

function PredictButton({ onClick }) {
  return (
    <div>
      <Button
        variant="contained"
        onClick={onClick}
        sx={{
          backgroundColor: '#8B0000', // Dark red, similar to "blood red"
          '&:hover': {
            backgroundColor: '#640000', // A darker shade for hover state
          },
        }}
      >
        Predict Fight
      </Button>
    </div>
  );
}

export default PredictButton;
