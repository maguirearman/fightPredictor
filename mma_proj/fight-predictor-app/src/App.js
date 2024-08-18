// App.js
import './App.css';
import React, { useState, useEffect } from 'react';
import FighterSelector from './FighterSelector';
import PredictButton from './PredictButton';
import { ThemeProvider} from '@mui/material/styles'; // Import ThemeProvider
import Grid from '@mui/material/Grid'; // Import Grid component
import Box from '@mui/material/Box'; // Import Box component
import theme from './theme.js'; // Import the custom theme
import FighterCard from './FighterCard';
import { fighterCardData, top15Flyweight, top15Bantamweight, top15Featherweight, top15Lightweight, top15Welterweight, top15Middleweight, top15LightHeavyweight, top15Heavyweight } from './data/fighterCardData';
import Typography from '@mui/material/Typography';

// Define the main App component
function App() {

  // State to store the list of fighters
  const [fighters, setFighters] = useState([]);
  // State to track the selected weight class and fighter
  const [selectedFighter1, setSelectedFighter1] = useState('');
  const [selectedFighter2, setSelectedFighter2] = useState('');
  //Add state to track predicted winner
  const [predictionResult, setPredictionResult] = useState('');
  // Add state hooks to store the probabilities
  const [fighter1Prob, setFighter1Prob] = useState('');
  const [fighter2Prob, setFighter2Prob] = useState('');


  // Event handlers to select a fighter
  const handleSelectFighter1 = (fighter) => {
    setSelectedFighter1(fighter);
  };
  const handleSelectFighter2 = (fighter) => {
    setSelectedFighter2(fighter);
  };

  // Event handler to predict the fight
  const handlePredictFight = () => {
    const data = {
      fighter1: selectedFighter1,
      fighter2: selectedFighter2
    };
    // Make a POST request to the backend to predict the fight
    fetch('/api/predict', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
      // Log the response from the backend
      console.log('Response from backend:', data);
      // Set the prediction result to be displayed
      setPredictionResult(`Predicted Winner: ${data.predicted_winner}`);
      setFighter1Prob(data.fighter1_probability);
      setFighter2Prob(data.fighter2_probability);
    })
    .catch(error => {
      console.error('Error:', error);
      setPredictionResult('Failed to predict the fight.');
    }); 
    console.log('Predicting fight...');
  };

  // Fetch fighters data from the server on component mount
  useEffect(() => {
    fetch('/api/fighters')
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
  
  // Render the main App component
  return (
    <ThemeProvider theme={theme}> 
            <Box sx={{ flexGrow: 1, padding: 3 }}> {/* Add padding around the entire app */}
        <Grid container spacing={2} justifyContent="center"> {/* Reduced spacing from 3 to 2 */}
          <Grid item xs={12}>
            <Box textAlign="center">
              <h1>
                MMA Fight Predictor
                <Typography component="span" variant="h6" color="text.secondary" style={{ display: 'block', fontSize: '0.5em' }}>
                  by Maguire Arman
                </Typography>
              </h1>
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
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <Box textAlign="center">
                  <h1>Fight Prediction Results</h1>
                  {predictionResult && <p> {predictionResult}</p>}
                  {fighter1Prob && <p> {fighter1Prob}</p>}
                  {fighter2Prob && <p> {fighter2Prob}</p>}
                </Box>
              </Grid>
            </Grid>
          )}
          {/* Fighter Cards Section */}
          <Grid item xs={12}>
            <Box textAlign="center">
              <h1>Top 15 Pound For Pound</h1>
            </Box>
          </Grid>
          {fighterCardData.map(fighter => (
            <Grid item xs={6} sm={4} md={3} lg={2} key={fighter.id}>
              <FighterCard fighter={fighter} />
            </Grid>
          ))}
          {/* Fighter Cards Section */}
          <Grid item xs={12}>
            <Box textAlign="center">
              <h1>Top 15 Flyweight</h1>
            </Box>
          </Grid>
          {top15Flyweight.map(fighter => (
            <Grid item xs={6} sm={4} md={3} lg={2} key={fighter.id}>
              <FighterCard fighter={fighter} />
            </Grid>
          ))}
          <Grid item xs={12}>
            <Box textAlign="center">
              <h1>Top 15 Bantamweight</h1>
            </Box>
          </Grid>
          {top15Bantamweight.map(fighter => (
            <Grid item xs={6} sm={4} md={3} lg={2} key={fighter.id}>
              <FighterCard fighter={fighter} />
            </Grid>
          ))}
          <Grid item xs={12}>
            <Box textAlign="center">
              <h1>Top 15 Featherweight</h1>
            </Box>
          </Grid>
          {top15Featherweight.map(fighter => (
            <Grid item xs={6} sm={4} md={3} lg={2} key={fighter.id}>
              <FighterCard fighter={fighter} />
            </Grid>
          ))}
          <Grid item xs={12}>
            <Box textAlign="center">
              <h1>Top 15 Lightweight</h1>
            </Box>
          </Grid>
          {top15Lightweight.map(fighter => (
            <Grid item xs={6} sm={4} md={3} lg={2} key={fighter.id}>
              <FighterCard fighter={fighter} />
            </Grid>
          ))}
          <Grid item xs={12}>
            <Box textAlign="center">
              <h1>Top 15 Welterweight</h1>
            </Box>
          </Grid>
          {top15Welterweight.map(fighter => (
            <Grid item xs={6} sm={4} md={3} lg={2} key={fighter.id}>
              <FighterCard fighter={fighter} />
            </Grid>
          ))}
          <Grid item xs={12}>
            <Box textAlign="center">
              <h1>Top 15 Middleweight</h1>
            </Box>
          </Grid>
          {top15Middleweight.map(fighter => (
            <Grid item xs={6} sm={4} md={3} lg={2} key={fighter.id}>
              <FighterCard fighter={fighter} />
            </Grid>
          ))}
          <Grid item xs={12}>
            <Box textAlign="center">
              <h1>Top 15 Light Heavyweight</h1>
            </Box>
          </Grid>
          {top15LightHeavyweight.map(fighter => (
            <Grid item xs={6} sm={4} md={3} lg={2} key={fighter.id}>
              <FighterCard fighter={fighter} />
            </Grid>
          ))}
          <Grid item xs={12}>
            <Box textAlign="center">
              <h1>Top 15 Heavyweight</h1>
            </Box>
          </Grid>
          {top15Heavyweight.map(fighter => (
            <Grid item xs={6} sm={4} md={3} lg={2} key={fighter.id}>
              <FighterCard fighter={fighter} />
            </Grid>
          ))}
          
        </Grid>
      </Box>
    </ThemeProvider>
  );
}

export default App;
