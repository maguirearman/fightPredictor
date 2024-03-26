// App.js
import React, { useState, useEffect } from 'react';
import WeightClassSelector from './WeightClassSelector';
import FighterSelector from './FighterSelector';
import PredictButton from './PredictButton'; 

function App() {
  // Define some dummy weight classes and fighters
  const weightClasses = ['Flyweight', 'Bantamweight', 'Featherweight', 'Lightweight', 'Welterweight', 'Middleweight', 'Light Heavyweight', 'Heavyweight', 'Womens Strawweight', 'Womens Flyweight', 'Womens Bantamweight'];
  const [fighters, setFighters] = useState([]);


  // State to track the selected weight class and fighter
  const [selectedWeightClass, setSelectedWeightClass] = useState('');
  const [selectedFighter1, setSelectedFighter1] = useState('');
  const [selectedFighter2, setSelectedFighter2] = useState('');

  // Functions to handle selecting weight class and fighters
  const handleSelectWeightClass = (weightClass) => {
    setSelectedWeightClass(weightClass);
    if (weightClass) {
      fetchFighters(weightClass);
    }
  };


  const fetchFighters = (weightClass) => {
    // Send a request to the backend to fetch fighters for the selected weight class
    fetch(`http://127.0.0.1:5000/fighters?weightClass=${weightClass}`, {
      method: 'GET',
      mode: 'cors'
    })
      .then(response => response.json())
      .then(data => {
        setFighters(data);
      })
      .catch(error => {
        console.error('Error fetching fighters:', error);
      });
  };

  const handleSelectFighter1 = (fighter) => {
    setSelectedFighter1(fighter);
  };

  const handleSelectFighter2 = (fighter) => {
    setSelectedFighter2(fighter);
  };


  const handlePredictFight = () => {
    const data = {
      weightClass: selectedWeightClass,
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
      // Handle the response as needed
    })
    .catch(error => {
      console.error('Error:', error);
      // Handle errors
    }); 
      // Perform prediction logic here
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
    <div className="App">
      <h1>MMA Fight Predictor</h1>
      <WeightClassSelector
        weightClasses={weightClasses}
        selectedWeightClass={selectedWeightClass}
        onSelectWeightClass={handleSelectWeightClass}
      />
      <FighterSelector
        fighters={fighters}
        selectedFighter={selectedFighter1}
        onSelectFighter={handleSelectFighter1}
        label={`Select Fighter 1: ${selectedFighter1}`}
      />
      <FighterSelector
        fighters={fighters}
        selectedFighter={selectedFighter2}
        onSelectFighter={handleSelectFighter2}
        label={`Select Fighter 2: ${selectedFighter2}`}
      />
      <PredictButton onClick={handlePredictFight} /> {/* Add PredictButton component with onClick prop */}
    </div>
  );
}

export default App;
