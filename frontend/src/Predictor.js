import React, { useState } from 'react';
import axios from 'axios';
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

    // Validate sequence length
    if (sequence.length !== 57) {
      setError('Sequence must be exactly 57 nucleotides long.');
      setLoading(false);
      return;
    }

    try {
      const res = await axios.post('https://dnasequence.onrender.com/predict', {
        sequence: sequence.toLowerCase(),
      });

      console.log('Server response:', res.data);

      if (res.data && (res.data.class !== undefined || res.data.error || res.data.message)) {
        setResponse(res.data);
      } else {
        setError('Unexpected response format from server.');
      }
    } catch (err) {
      console.error('Request error:', err);
      setError(err.response?.data?.error || 'An error occurred while making the prediction.');
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
          placeholder="Enter a DNA sequence of 57 nucleotides"
          value={sequence}
          onChange={(e) => setSequence(e.target.value)}
          maxLength={57}
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
          <p>
            <strong>ID:</strong> {response.id || 'N/A'}
          </p>
          <p>{response.message || 'Prediction completed successfully.'}</p>
        </div>
      )}
    </div>
  );
};

export default Predictor;
