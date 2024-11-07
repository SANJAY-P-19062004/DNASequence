import React, { useState } from 'react';
import axios from 'axios';

const Predictor = () => {
    const [sequence, setSequence] = useState('');
    const [result, setResult] = useState(null);
    const [error, setError] = useState('');

    const handleInputChange = (e) => {
        setSequence(e.target.value);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setResult(null);

        if (sequence.length !== 57) {
            setError('Sequence must be exactly 57 nucleotides long.');
            return;
        }

        try {
            const response = await axios.post('https://dnasequence.onrender.com/predict', { sequence });
            setResult(response.data);
        } catch (err) {
            setError(err.response ? err.response.data.error : 'An error occurred');
        }
    };

    return (
        <div>
            <h1>DNA Sequence Predictor</h1>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    value={sequence}
                    onChange={handleInputChange}
                    placeholder="Enter 57-nucleotide sequence"
                    required
                />
                <button type="submit">Predict</button>
            </form>
            {result && (
                <div>
                    <h2>Prediction:</h2>
                    <p>Class: {result.class}</p>
                    <p>ID: {result.id}</p>
                </div>
            )}
            {error && <h2 style={{ color: 'red' }}>{error}</h2>}
        </div>
    );
};

export default Predictor;
