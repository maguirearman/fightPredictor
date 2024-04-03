// FighterSelector.js
import React from 'react';
import Select from 'react-select';

function FighterSelector({ fighters, selectedFighter, onSelectFighter, label }) {
  // Convert your fighters array for use with react-select
  // Assuming 'fighters' is an array of strings; adjust if it's an array of objects
  const options = fighters.map(fighter => ({ value: fighter, label: fighter }));
  
  // Handler for changes in the selection
  const handleChange = selectedOption => {
    // Call onSelectFighter with the value of the selected option
    onSelectFighter(selectedOption ? selectedOption.value : '');
  };

  // Find the currently selected option based on the selectedFighter prop
  const selectedOption = options.find(option => option.value === selectedFighter) || null;

  return (
    <div className="selector-container" style={{ width: '50%' }}>
      <label htmlFor={label.toLowerCase().replace(/\s+/g, '-')}>{label}</label>
      <Select
        inputId={label.toLowerCase().replace(/\s+/g, '-')} // ensures the label is properly associated with the react-select component
        value={selectedOption}
        onChange={handleChange}
        options={options}
        isClearable={true} // Allows users to clear the selected value
        placeholder="Select a fighter"
      />
    </div>
  );
}

export default FighterSelector;