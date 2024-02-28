// WeightClassSelector.js

import React from 'react';

function WeightClassSelector({ weightClasses, selectedWeightClass, onSelectWeightClass }) {
  return (
    <div>
      <label htmlFor="weightClass">Select a Weight Class:</label>
      <select id="weightClass" value={selectedWeightClass} onChange={(e) => onSelectWeightClass(e.target.value)}>
        <option value="">Select</option>
        {weightClasses.map((weightClass) => (
          <option key={weightClass} value={weightClass}>
            {weightClass}
          </option>
        ))}
      </select>
    </div>
  );
}

export default WeightClassSelector;
