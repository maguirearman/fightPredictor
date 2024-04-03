// WeightClassSelector.js
import React from 'react';
import Select from 'react-select';

function WeightClassSelector({ weightClasses, selectedWeightClass, onSelectWeightClass }) {
  // Convert your weightClasses array for use with react-select
  const options = weightClasses.map(weightClass => ({
    value: weightClass,
    label: weightClass // The text that will be displayed
  }));

  const handleChange = selectedOption => {
    // Call onSelectWeightClass with the value of the selected option
    // or an empty string if no option is selected (cleared selection)
    onSelectWeightClass(selectedOption ? selectedOption.value : '');
  };

  // Find the currently selected option
  const selectedOption = options.find(option => option.value === selectedWeightClass) || null;

  return (
    <div className='weight-selector'>
      <label htmlFor="weight-class-select">Select a Weight Class:</label>
      <Select
        inputId="weight-class-select" // Ensures the label is properly associated
        value={selectedOption}
        onChange={handleChange}
        options={options}
        isClearable={true} // Allows users to clear the selected value
        placeholder="Select a weight class"
      />
    </div>
  );
}

export default WeightClassSelector;