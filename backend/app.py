from flask import Flask, jsonify, request
from flask_cors import CORS
import joblib
import numpy as np

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load the saved model
model = joblib.load('model1.pkl')

def encode_sequence(sequence):
    # Mapping nucleotides to numbers
    mapping = {'a': 0, 't': 1, 'c': 2, 'g': 3}
    encoded = []
    for nucleotide in sequence.lower():
        if nucleotide in mapping:
            encoded.append(mapping[nucleotide])
        else:
            raise ValueError(f"Invalid nucleotide: {nucleotide}")
    return np.array(encoded).reshape(1, -1)  # Reshape for model input

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get JSON data from request
        data = request.get_json(force=True)
        sequence = data.get('sequence', '')
        
        if not sequence or len(sequence) != 57:
            return jsonify({'error': 'Invalid sequence. Must be 57 nucleotides long.'}), 400
        
        # Encode the sequence
        sequence_vector = encode_sequence(sequence)
        
        # Make prediction
        prediction = model.predict(sequence_vector)
        
        return jsonify({'class': str(prediction[0])})
    
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
