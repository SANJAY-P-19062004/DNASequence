from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import joblib
import numpy as np

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the trained model
model = joblib.load('model.pkl')

# Function to convert nucleotide sequence to numerical format
def convert_sequence(sequence):
    nucleotide_mapping = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
    numerical_sequence = np.array([nucleotide_mapping.get(nuc, -1) for nuc in sequence]).reshape(1, -1)
    return numerical_sequence

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    sequence = data.get('sequence', '')

    if len(sequence) != 57:
        return jsonify({'error': 'Sequence must be exactly 57 nucleotides long.'}), 400

    numerical_sequence = convert_sequence(sequence)

    prediction = model.predict(numerical_sequence)
    result = '+' if prediction[0] == 1 else '-'

    return jsonify({'prediction': result})

if __name__ == '__main__':
    app.run(debug=True)
