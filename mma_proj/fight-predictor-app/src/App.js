// App.js
import './App.css';
import React, { useState, useEffect } from 'react';
// import WeightClassSelector from './WeightClassSelector';
import FighterSelector from './FighterSelector';
import PredictButton from './PredictButton';
import { ThemeProvider} from '@mui/material/styles'; // Import ThemeProvider
import Grid from '@mui/material/Grid'; // Import Grid component
import Box from '@mui/material/Box'; // Import Box component
import theme from './theme.js'; // Import the custom theme
 

function App() {
  // Define some dummy weight classes and fighters
  // const weightClasses = ['Flyweight', 'Bantamweight', 'Featherweight', 'Lightweight', 'Welterweight', 'Middleweight', 'Light Heavyweight', 'Heavyweight', 'Womens Strawweight', 'Womens Flyweight', 'Womens Bantamweight'];
  const [fighters, setFighters] = useState([]);


  // State to track the selected weight class and fighter
  // const [selectedWeightClass, setSelectedWeightClass] = useState('');
  const [selectedFighter1, setSelectedFighter1] = useState('');
  const [selectedFighter2, setSelectedFighter2] = useState('');

  //Add state to track predicted winner
  const [predictionResult, setPredictionResult] = useState('');

  // // Functions to handle selecting weight class and fighters
  // const handleSelectWeightClass = (weightClass) => {
  //   setSelectedWeightClass(weightClass);
  //   if (weightClass) {
  //     fetchFighters(weightClass);
  //   }
  // };


  // const fetchFighters = (weightClass) => {
  //   // Send a request to the backend to fetch fighters for the selected weight class
  //   fetch(`http://127.0.0.1:5000/fighters?weightClass=${weightClass}`, {
  //     method: 'GET',
  //     mode: 'cors'
  //   })
  //     .then(response => response.json())
  //     .then(data => {
  //       setFighters(data);
  //     })
  //     .catch(error => {
  //       console.error('Error fetching fighters:', error);
  //     });
  // };

  const handleSelectFighter1 = (fighter) => {
    setSelectedFighter1(fighter);
  };

  const handleSelectFighter2 = (fighter) => {
    setSelectedFighter2(fighter);
  };

  const handlePredictFight = () => {
    const data = {
      // weightClass: selectedWeightClass,
      fighter1: selectedFighter1,
      fighter2: selectedFighter2
    };
  
    fetch('http://127.0.0.1:5000/predict', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
      console.log('Response from backend:', data);
      // Set the prediction result to be displayed
      setPredictionResult(`Predicted Winner: ${data.prediction}`);
    })
    .catch(error => {
      console.error('Error:', error);
      setPredictionResult('Failed to predict the fight.');
    }); 
    console.log('Predicting fight...');
  };

  // Fetch fighters data from the server on component mount
  useEffect(() => {
    fetch('http://127.0.0.1:5000/fighters')
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        setFighters(data);
        console.log('Fetched fighters:', data);
      })
      .catch(error => {
        console.error('Error fetching fighters:', error);
      });
  }, []); // Empty dependency array means this effect runs only once on component mount
  

  return (
    <ThemeProvider theme={theme}> 
      <Box sx={{ flexGrow: 1, padding: 3 }}> {/* Add padding around the entire app */}
        <Grid container spacing={3} justifyContent="center"> {/* Add spacing between items and center them */}
          <Grid item xs={12}>
            <Box textAlign="center">
              <h1>MMA Fight Predictor</h1>
              </Box>
          </Grid>
          <Grid item md={6} sm={8} xs={12}>
            <FighterSelector
              fighters={fighters}
              selectedFighter={selectedFighter1}
              onSelectFighter={handleSelectFighter1}
              label={`Select Fighter 1`}
            />
          </Grid>
          <Grid item md={6} sm={8} xs={12}>
            <FighterSelector
              fighters={fighters}
              selectedFighter={selectedFighter2}
              onSelectFighter={handleSelectFighter2}
              label={`Select Fighter 2`}
            />
          </Grid>
          <Grid item xs={12}>
            <Box textAlign="center"> {/* Center the PredictButton */}
              <PredictButton onClick={handlePredictFight} />
            </Box>
          </Grid>
          {predictionResult && (
            <Grid item xs={12}>
              <Box textAlign="center"> {/* Center the prediction result */}
                <div className="prediction-result">{predictionResult}</div>
              </Box>
            </Grid>
          )}
        </Grid>
      </Box>
    </ThemeProvider>
  );
}

export default App;
