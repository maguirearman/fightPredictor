// FighterSelector.js
import React from 'react';
// import Select from 'react-select';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';

function FighterSelector({ fighters, selectedFighter, onSelectFighter, label }) {
  // Prepare the options in the expected format if not already
  const options = fighters.map(fighter => (typeof fighter === 'string' ? { label: fighter, value: fighter } : fighter));

  // Handle selection change
  const handleChange = (event, newValue) => {
    onSelectFighter(newValue ? newValue.value : '');
  };

  // Determine the value based on the selectedFighter
  const value = options.find(option => option.value === selectedFighter) || null;

  return (
    <Autocomplete
      value={value}
      onChange={handleChange}
      options={options}
      getOptionLabel={(option) => option.label}
      isOptionEqualToValue={(option, value) => option.value === value.value}
      renderInput={(params) => (
        <TextField
          {...params}
          label={label}
          variant="outlined"
          // Add custom styling here
          InputProps={{
            ...params.InputProps,
            style: { backgroundColor: 'white' }, // Makes the input field white
          }}
        />
      )}
      fullWidth
      // Apply sx prop for styling
      sx={{
        width: '50%', // Sets the width to half of its container
        '& .MuiOutlinedInput-root': {
          '& fieldset': {
            borderColor: 'gray', // Changes the border color, adjust as needed
          },
          '&:hover fieldset': {
            borderColor: 'black', // Changes the border color on hover, adjust as needed
          },
          '&.Mui-focused fieldset': {
            borderColor: 'primary.main', // Changes the border color when focused to the theme's primary color
          },
        },
      }}
      clearOnEscape
    />
  );
}

export default FighterSelector;