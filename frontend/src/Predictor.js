import React, { useState } from 'react';
import './index.css';

const Predictor = () => {
  const [sequence, setSequence] = useState('');
  const [response, setResponse] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setResponse(null);
    setError('');
    setLoading(true);

    try {
      // Using fetch to send a POST request
      const res = await fetch('https://dnasequence.onrender.com/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ sequence: sequence.toLowerCase() }),
      });

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.error || 'An error occurred while making the prediction.');
      }

      const data = await res.json();
      console.log('Server response:', data);

      if (data && (data.class !== undefined || data.error || data.message)) {
        setResponse(data);
      } else {
        setError('Unexpected response format from server.');
      }
    } catch (err) {
      console.error('Request error:', err);
      setError(err.message || 'An error occurred while making the prediction.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>DNA Sequence Classifier</h1>
      <form onSubmit={handleSubmit} className="form">
        <textarea
          className="textarea"
          placeholder="Enter a DNA sequence"
          value={sequence}
          onChange={(e) => setSequence(e.target.value)}
          rows={4}
          required
        />
        <button type="submit" className="button" disabled={loading}>
          {loading ? 'Predicting...' : 'Predict'}
        </button>
      </form>

      {error && <p className="error">{error}</p>}
      {response && response.class && (
        <div className="result">
          <p>
            <strong>Class:</strong> {response.class === '+' ? 'Promoter' : 'Non-Promoter'}
          </p>
          
          <p>{response.message || 'Prediction completed successfully.'}</p>
        </div>
      )}
    </div>
  );
};

export default Predictor;
