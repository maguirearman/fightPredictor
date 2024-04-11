// FighterSelector.js
import React from 'react';
// import Select from 'react-select';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';

function FighterSelector({ fighters, selectedFighter, onSelectFighter, label }) {
  const options = fighters.map(fighter => (typeof fighter === 'string' ? { label: fighter, value: fighter } : fighter));

  const handleChange = (event, newValue) => {
    onSelectFighter(newValue ? newValue.value : '');
  };

  const value = options.find(option => option.value === selectedFighter) || null;

  return (
    <div style={{ display: 'flex', justifyContent: 'center', height: '100%' }}>
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
            InputProps={{
              ...params.InputProps,
              style: { backgroundColor: 'white' }, // Makes the input field white
            }}
          />
        )}
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
    </div>
  );
}

export default FighterSelector;

