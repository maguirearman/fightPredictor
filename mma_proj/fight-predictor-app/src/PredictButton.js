// PredictButton.js

import React from 'react';

function PredictButton({ onClick }) {
  return (
    <div>
      <button onClick={onClick}>Predict Fight</button>
    </div>
  );
}

export default PredictButton;
