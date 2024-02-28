// FighterSelector.js

import React from 'react';

function FighterSelector({ fighters, selectedFighter, onSelectFighter }) {
  return (
    <div>
      <label htmlFor="fighter">Select a Fighter:</label>
      <select id="fighter" value={selectedFighter} onChange={(e) => onSelectFighter(e.target.value)}>
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
