// PredictButton.js

import React from 'react';

function PredictButton({ onClick }) {
  return (
    <div>
      <button className="selector" onClick={onClick}>Predict Fight</button>
    </div>
  );
}

export default PredictButton;
