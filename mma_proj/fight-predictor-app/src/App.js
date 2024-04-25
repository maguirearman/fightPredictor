// App.js
import './App.css';
import React, { useState, useEffect } from 'react';
import { Canvas } from '@react-three/fiber';
// import WeightClassSelector from './WeightClassSelector';
import FighterSelector from './FighterSelector';
import PredictButton from './PredictButton';
import { ThemeProvider} from '@mui/material/styles'; // Import ThemeProvider
import Grid from '@mui/material/Grid'; // Import Grid component
import Box from '@mui/material/Box'; // Import Box component
import theme from './theme.js'; // Import the custom theme
import FighterCard from './FighterCard';
import Typography from '@mui/material/Typography';
import Experience from './Experience.jsx';
 

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


  // Manually defined fighters data
  const fighterCardData = [
    {
      id: 1,
      name: "Islam Makhachev",
      image: "https://dmxg5wxfqgb4u.cloudfront.net/styles/athlete_bio_full_body/s3/2023-10/MAKHACHEV_ISLAM_BELT_L_10-21.png?itok=glu3eHJa",
      ranking: "#1 Pound for Pound, Lightweight Champion",
      weightClass: "Lightweight"
    },
    {
      id: 2,
      name: "Jon Jones",
      image: "https://dmxg5wxfqgb4u.cloudfront.net/styles/athlete_bio_full_body/s3/2023-03/JONES_JON_L_BELT_03_04.png?itok=P6J6DQpm",
      ranking: "#1 Pound for Pound, Heavyweight Champion",
      weightClass: "Heavyweight"
    },
    {
      id: 3,
      name: "Leon Edwards",
      image: "https://dmxg5wxfqgb4u.cloudfront.net/styles/athlete_bio_full_body/s3/2023-12/EDWARDS_LEON_BELT_L_12-16.png?itok=RVcuzrpG",
      ranking: "#3 Pound for Pound, Welterweight Champion",
      weightClass: "Welterweight"
    },
    {
      id: 4,
      name: "Alex Pereira",
      image: "https://dmxg5wxfqgb4u.cloudfront.net/styles/athlete_bio_full_body/s3/2024-04/PEREIRA_ALEX_L_BELT_04-13.png?itok=-zKSPFcu",
      ranking: "#4 Pound for Pound, Light Heavyweight Champion, Former Middleweight Champion",
      weightClass: "Light Heavyweight"
    },
    {
      id: 5,
      name: "Ilia Topuria",
      image: "https://dmxg5wxfqgb4u.cloudfront.net/styles/athlete_bio_full_body/s3/2024-02/TOPURIA_ILIA_L_BELT_02-17.png?itok=h1fu9Vu9",
      ranking: "#5 Pound for Pound, Featherweight Champion",
      weightClass: "Featherweight"

    }, 
    {
      id: 6,
      name: "Sean O'Malley",
      image: "https://dmxg5wxfqgb4u.cloudfront.net/styles/athlete_bio_full_body/s3/2024-03/OMALLEY_SEAN_BELT_L_03-09.png?itok=1XrvvVTW",
      ranking: "#6 Pound for Pound, Bantamweight Champion",
      weightClass: "Bantamweight"
    },
    {
      id: 7,
      name: "Alexander Volkanovski",
      image: "https://dmxg5wxfqgb4u.cloudfront.net/styles/athlete_bio_full_body/s3/2024-02/VOLKANOVSKI_ALEXANDER_L_02-17.png?itok=Vu9a3K_h",
      ranking: "#7 Pound for Pound, Featherweight Champion",
      weightClass: "Featherweight"
    },
    {
      id: 8,
      name: "Max Holloway",
      image: "https://dmxg5wxfqgb4u.cloudfront.net/styles/athlete_bio_full_body/s3/2024-04/HOLLOWAY_MAX_L_04-13.png?itok=U9IB8OUQ",
      ranking: "#8 Pound for Pound, BMF Champion, #9 Lightweight, #2 Featherweight",
      weightClass: "Featherweight, Lightweight"
    },
    {
      id: 9,
      name: "Dricus Du Plessis",
      image: "https://dmxg5wxfqgb4u.cloudfront.net/styles/athlete_bio_full_body/s3/2024-01/DU_PLESSUS_DRICUS_L_BELTMOCK.png?itok=Te4zddjX",
      ranking: "#9 Pound for Pound, Middleweight Champion",
      weightClass: "Middleweight"
    }, 
    {
      id: 10,
      name: "Alexandre Pantoja",
      image: "https://dmxg5wxfqgb4u.cloudfront.net/styles/athlete_bio_full_body/s3/2023-12/PANTOJA_ALEXANDRE_L_12-16.png?itok=KUFPMuog",
      ranking: "#10 Pound for Pound, Flyweight Champion",
      weightClass: "Flyweight"
    },
    {
      id: 11,
      name: "Charles Oliveira",
      image: "https://dmxg5wxfqgb4u.cloudfront.net/styles/athlete_bio_full_body/s3/2024-04/OLIVEIRA_CHARLES_L_04-13.png?itok=zuTsqmoN",
      ranking: "#11 Pound for Pound, #2 Lightweight",
      weightClass: "Lightweight"
    },
    {
      id: 12,
      name: "Israel Adesanya",
      image: "https://dmxg5wxfqgb4u.cloudfront.net/styles/athlete_bio_full_body/s3/2023-09/ADESANYA_ISRAEL_L_04-08.png?itok=FOMzxCwD",
      ranking: "#12 Pound for Pound, #2 Middleweight",
      weightClass: "Middleweight"
    },
    {
      id: 13,
      name: "Tom Aspinall",
      image: "https://dmxg5wxfqgb4u.cloudfront.net/styles/athlete_bio_full_body/s3/2024-01/ASPINALL_TOM_L_BELTMOCK.png?itok=b-8iWaRT",
      ranking: "#13 Pound for Pound, Interim Heavyweight Champion",
      weightClass: "Heavyweight"
    }, 
    {
      id: 14,
      name: "Sean Strickland",
      image: "https://dmxg5wxfqgb4u.cloudfront.net/styles/athlete_bio_full_body/s3/2023-06/STRICKLAND_SEAN_L_07-01.png?itok=Xa9H8rts",
      ranking: "#14 Pound for Pound, #1 Middleweight",
      weightClass: "Middleweight"
    }, 
    {
      id: 15,
      name: "Aljermain Sterling",
      image: "https://dmxg5wxfqgb4u.cloudfront.net/styles/athlete_bio_full_body/s3/2024-04/STERLING_ALJAMAIN_L_04-13.png?itok=T1vPSqkE",
      ranking: "#15 Pound for Pound, #8 Featherweight",
      weightClass: "Bantamweight"
    }

    // Add more fighters as needed
  ];



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
    <>
    <Canvas
      style={{ height: '100vh', width: '100vw' }}
    >
      <color attach="background" args={['#000000']} />
      <Experience />
    </Canvas>
    <ThemeProvider theme={theme}> 
      <Box sx={{ flexGrow: 1, padding: 3 }}> {/* Add padding around the entire app */}
        <Grid container spacing={2} justifyContent="center"> {/* Reduced spacing from 3 to 2 */}
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
          {/* Fighter Cards Section */}
          <Grid item xs={12}>
            <Typography variant="h4" component="div" gutterBottom>
              Top Fighters
            </Typography>
          </Grid>
          {fighterCardData.map(fighter => (
            <Grid item xs={12} sm={6} md={4} key={fighter.id}>
              <FighterCard fighter={fighter} />
            </Grid>
          ))}
        </Grid>
      </Box>
    </ThemeProvider>
    </>
  );
}

export default App;
