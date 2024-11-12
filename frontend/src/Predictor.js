// App.js
import React, { useState } from 'react';
import './index.css';

const Predictor = () => {
  const [sequence, setSequence] = useState('');
  const [prediction, setPrediction] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleInputChange = (e) => {
    setSequence(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setPrediction('');

    try {
      const response = await fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ sequence: sequence }),
      });
      
      const data = await response.json();
      if (data.error) {
        setError(data.error);
      } else {
        setPrediction(data.prediction);
      }
    } catch (err) {
      setError('Error occurred while making the prediction.');
    }
    setLoading(false);
  };

  return (
    <div className="container">
      <h1>Promoter Gene Sequence Classifier</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Gene Sequence:
          <textarea
            value={sequence}
            onChange={handleInputChange}
            rows="4"
            cols="50"
            placeholder="Enter gene sequence here..."
          />
        </label>
        <button type="submit" disabled={loading}>
          {loading ? 'Processing...' : 'Predict'}
        </button>
      </form>

      {prediction && (
        <div className="result">
          <h2>Prediction Result:</h2>
          <p>{`This sequence is a ${prediction === '1' ? 'Promoter' : 'Non-Promoter'}`}</p>
        </div>
      )}

      {error && <p className="error">{error}</p>}
    </div>
  );
};

export default Predictor;
