import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const response = await fetch('http://localhost:9876/api/data');
      if (!response.ok) {
        throw new Error('Failed to fetch data');
      }
      const jsonData = await response.json();
      setData(jsonData);
    } catch (error) {
      console.error('Error:', error.message);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Average Calculator Microservice</h1>
        {data && (
          <div>
            <h2>Previous Window State</h2>
            <p>Numbers: {data.windowPrevState.join(', ')}</p>
            <h2>Current Window State</h2>
            <p>Numbers: {data.windowCurrState.join(', ')}</p>
            <h2>All Numbers</h2>            <p>Numbers: {data.numbers.join(', ')}</p>
            <h2>Average</h2>
            <p>{data.average}</p>
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
