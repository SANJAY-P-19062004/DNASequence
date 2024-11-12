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

    if (sequence.length !== 57) {
      setError('Sequence must be exactly 57 nucleotides long.');
      return;
    }

    try {
      const res = await axios.post('https://dnasequence.onrender.com/predict', { sequence });
      setResponse(res.data);
    } catch (err) {
      if (err.response) {
        setError(err.response.data.error);
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
                <strong>Class:</strong> {response.class}
              </p>
              <p>
                <strong>ID:</strong> {response.id}
              </p>
              <p>{response.message}</p>
            </>
          ) : (
            <p>{response.message}</p>
          )}
        </div>
      )}
    </div>
  );
};

export default Predictor;
