import React, { useState } from 'react';
import axios from 'axios';
import './index.css';

const Predictor = () => {
  const [sequence, setSequence] = useState('');
  const [response, setResponse] = useState(null);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setResponse(null);
    setError('');

    // Validate sequence length
    if (sequence.length !== 57) {
      setError('Sequence must be exactly 57 nucleotides long.');
      return;
    }

    try {
      console.log('Sending request to the server...');
      const res = await axios.post('https://dnasequence.onrender.com/predict', { sequence: sequence.toLowerCase() });

      // Debugging output
      console.log('Raw server response:', res);
      console.log('Response data:', res.data);

      // Check if response data has the expected structure
      if (res.data && (res.data.class || res.data.error || res.data.message)) {
        setResponse(res.data);
      } else {
        setError('Unexpected response format from server.');
        console.error('Unexpected server response:', res.data);
      }
    } catch (err) {
      console.error('Error:', err);
      if (err.response) {
        setError(err.response.data.error || 'Prediction failed. Please try again.');
      } else {
        setError('Server error. Please try again later.');
      }
    }
  };

  return (
    <div className="container">
      <h1>DNA Sequence Classifier</h1>
      <form onSubmit={handleSubmit} className="form">
        <textarea
          className="textarea"
          placeholder="Enter a DNA sequence of 57 nucleotides"
          value={sequence}
          onChange={(e) => setSequence(e.target.value)}
          maxLength={57}
          rows={4}
        />
        <button type="submit" className="button">
          Predict
        </button>
      </form>
      {error && <p className="error">{error}</p>}
      {response && (
        <div className="result">
          {response.class ? (
            <>
              <p>
                <strong>Class:</strong> {response.class === '+' ? 'Promoter' : 'Non-Promoter'}
              </p>
              <p>
                <strong>ID:</strong> {response.id || 'N/A'}
              </p>
              <p>{response.message || 'Prediction completed successfully.'}</p>
            </>
          ) : (
            <p>{response.error || response.message || 'No data returned from server.'}</p>
          )}
        </div>
      )}
    </div>
  );
};

export default Predictor;
