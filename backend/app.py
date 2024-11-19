from flask import Flask, jsonify, request
from flask_cors import CORS
import joblib
import numpy as np
import logging

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/predict": {"origins": "*"}})
logging.basicConfig(level=logging.DEBUG)

# Load the saved model
model = joblib.load('model1.pkl')

def encode_sequence(sequence, target_length=228):
    # Mapping nucleotides to numbers
    mapping = {'a': 0, 't': 1, 'c': 2, 'g': 3}
    encoded = []

    # Encode the sequence
    for nucleotide in sequence.lower():
        if nucleotide in mapping:
            encoded.append(mapping[nucleotide])
        else:
            raise ValueError(f"Invalid nucleotide: {nucleotide}")
    
    # Adjust the sequence to match the target length
    if len(encoded) > target_length:
        # Trim if it's longer than required
        encoded = encoded[:target_length]
    elif len(encoded) < target_length:
        # Pad with zeros if it's shorter than required
        encoded += [0] * (target_length - len(encoded))

    return np.array(encoded).reshape(1, -1)  # Reshape for model input

@app.route('/predict', methods=['POST'])
def predict():
    try:
        logging.debug(f"Request headers: {request.headers}")
        logging.debug(f"Request data: {request.data}")

        data = request.get_json(force=True)
        logging.debug(f"Parsed JSON data: {data}")

        sequence = data.get('sequence', '')
        
        # Validate sequence
        if not sequence or len(sequence) == 0:
            return jsonify({'error': 'Sequence cannot be empty.'}), 400
        
        # Encode the sequence to match model's input
        sequence_vector = encode_sequence(sequence)
        
        # Make prediction
        prediction = model.predict(sequence_vector)
        logging.debug(f"Model prediction: {prediction}")

        # Map prediction to class
        predicted_class = '+' if prediction[0] == '+' else '-'
        return jsonify({'class': predicted_class, 'id': 'Unknown', 'message': 'Prediction successful'})

    except ValueError as ve:
        logging.error(f"ValueError: {ve}")
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        logging.error(f"Exception: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
