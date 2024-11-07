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
            const response = await axios.post('https://dnasequence.onrender.com/predict', { sequence });

            // Update the prediction state with the result from backend
            setPrediction(response.data);
            setError('');
        } catch (err) {
            // Handle error response
            setPrediction(null);
            setError(err.response?.data?.error || 'Something went wrong');
        }
    };

    // Classify prediction as Promoter or Non-Promoter
    const getClassification = () => {
        if (prediction && prediction.prediction) {
            return prediction.prediction === '+' ? 'Promoter' : 'Non-Promoter';
        }
        return '';
    };

    return (
        <div>
            <h1>Sequence Classification</h1>
            <form onSubmit={handleSubmit}>
                <label>
                    Enter DNA Sequence:
                    <textarea
                        value={sequence}
                        onChange={(e) => setSequence(e.target.value)}
                        rows="4"
                        cols="50"
                    />
                </label>
                <button type="submit">Classify</button>
            </form>

            {prediction && (
                <div>
                    <h2>Prediction Result</h2>
                    <p><strong>Prediction:</strong> {prediction.prediction}</p>
                    <p><strong>Classification:</strong> {getClassification()}</p>
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
