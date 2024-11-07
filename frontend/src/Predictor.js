import React, { useState } from 'react';
import axios from 'axios';

const Predictor = () => {
    const [sequence, setSequence] = useState('');
    const [prediction, setPrediction] = useState(null);
    const [error, setError] = useState('');
    const [isValidSequence, setIsValidSequence] = useState(true);

    const validateSequence = (seq) => {
        // Check if the sequence is exactly 57 characters long
        return seq.length === 57;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        // Validate the sequence length
        if (!validateSequence(sequence)) {
            setError('Sequence must be exactly 57 characters long.');
            setPrediction(null);
            return;
        }

        try {
            // Check if the sequence exists in the dataset (assuming the dataset is accessible via URL)
            const datasetResponse = await axios.get('https://archive.ics.uci.edu/ml/machine-learning-databases/molecular-biology/promoter-gene-sequences/promoters.data');
            const dataset = datasetResponse.data; // Assuming it's a JSON array or object with sequences

            // Check if the sequence is in the dataset
            if (!dataset.includes(sequence)) {
                setError('Sequence not found in dataset.');
                setPrediction(null);
                return;
            }

            // Send the sequence to the backend for prediction
            const response = await axios.post('https://dnasequence.onrender.com/predict', { sequence });

            // Check if the backend returned an expected result
            if (response && response.data) {
                // Update the prediction state with the result from backend
                setPrediction(response.data);
                setError('');
            } else {
                setError('Invalid response from backend.');
                setPrediction(null);
            }
        } catch (err) {
            // Log the error to check the actual cause
            console.error('Error:', err);

            // Handle error response more specifically
            if (err.response) {
                // If there's a response from the backend
                setError(err.response?.data?.error || 'Something went wrong with the request');
            } else if (err.request) {
                // If the request was made but no response was received
                setError('No response received from the backend.');
            } else {
                // General error message
                setError('An error occurred while processing the request.');
            }

            setPrediction(null);
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

            {error && (
                <div>
                    <h2>Error</h2>
                    <p>{error}</p>
                </div>
            )}

            {prediction && (
                <div>
                    <h2>Prediction Result</h2>
                    <p><strong>Prediction:</strong> {prediction.prediction}</p>
                    <p><strong>Classification:</strong> {getClassification()}</p>
                </div>
            )}
        </div>
    );
};

export default Predictor;
