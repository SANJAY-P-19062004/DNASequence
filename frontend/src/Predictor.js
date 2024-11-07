import React, { useState } from 'react';
import axios from 'axios';

const Predictor = () => {
    const [sequence, setSequence] = useState('');
    const [prediction, setPrediction] = useState(null);
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            // Send the sequence to the backend for prediction
            const response = await axios.post(
                'https://dnasequence.onrender.com/predict', 
                { sequence },
                { timeout: 10000 }  // Timeout set to 10 seconds
            );

            // Update the prediction state with the result from the backend
            setPrediction(response.data);
            setError('');
        } catch (err) {
            // Handle error response
            setPrediction(null);
            setError(err.response?.data?.error || err.message || 'Something went wrong');
        }
    };

    return (
        <div>
            <h1>DNA Sequence Classification</h1>
            <form onSubmit={handleSubmit}>
                <label>
                    Enter DNA Sequence (57 nucleotides):
                    <textarea
                        value={sequence}
                        onChange={(e) => setSequence(e.target.value)}
                        rows="4"
                        cols="50"
                    />
                </label>
                <button type="submit">Classify</button>
            </form>

            {prediction && prediction.class && (
                <div>
                    <h2>Prediction Result</h2>
                    <p><strong>Class:</strong> {prediction.class === '+' ? 'Promoter' : 'Non-Promoter'}</p>
                    
                </div>
            )}

            {error && (
                <div>
                    <h2>Error</h2>
                    <p>{error}</p>
                </div>
            )}
        </div>
    );
};

export default Predictor;
