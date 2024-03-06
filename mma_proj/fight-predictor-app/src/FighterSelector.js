// FighterSelector.js

import React from 'react';

function FighterSelector({ fighters, selectedFighter, onSelectFighter, label }) {
  const selectId = label.toLowerCase().replace(/\s+/g, '-'); // Generate unique ID based on label

  return (
    <div>
      <label htmlFor={selectId}>Select a Fighter:</label>
      <select id={selectId} value={selectedFighter} onChange={(e) => onSelectFighter(e.target.value)}>
        <option value="">Select</option>
        {fighters.map((fighter) => (
          <option key={fighter} value={fighter}>
            {fighter}
          </option>
        ))}
      </select>
    </div>
  );
}


export default FighterSelector;
