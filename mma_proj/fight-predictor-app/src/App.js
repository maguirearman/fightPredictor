// App.js
import React, { useState } from 'react';
import WeightClassSelector from './WeightClassSelector';
import FighterSelector from './FighterSelector';

function App() {
  // Define some dummy weight classes and fighters
  const weightClasses = ['Flyweight', 'Bantamweight', 'Featherweight', 'Lightweight', 'Welterweight', 'Middleweight', 'Light Heavyweight', 'Heavyweight', 'Womens Strawweight', 'Womens Flyweight', 'Womens Bantamweight'];
  const fighters = ['Fighter 1', 'Fighter 2', 'Fighter 3', 'Fighter 4'];

  // State to track the selected weight class and fighter
  const [selectedWeightClass, setSelectedWeightClass] = useState('');
  const [selectedFighter1, setSelectedFighter1] = useState('');
  const [selectedFighter2, setSelectedFighter2] = useState('');

  // Functions to handle selecting weight class and fighters
  const handleSelectWeightClass = (weightClass) => {
    setSelectedWeightClass(weightClass);
  };

  const handleSelectFighter1 = (fighter) => {
    setSelectedFighter1(fighter);
  };

  const handleSelectFighter2 = (fighter) => {
    setSelectedFighter2(fighter);
  };

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
      />
      <FighterSelector
        fighters={fighters}
        selectedFighter={selectedFighter2}
        onSelectFighter={handleSelectFighter2}
      />
      {/* Add other components here */}
    </div>
  );
}

export default App;
