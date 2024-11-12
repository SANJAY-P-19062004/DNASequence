from flask import Flask, jsonify, request
from flask_cors import CORS
import joblib
import numpy as np

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the saved model
model = joblib.load('model1.pkl')

@app.route('/')
def home():
    return "Welcome to the Promoter Gene Sequence Classifier!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)
        sequence = data['sequence']
        nucleotides = list(sequence)
        nucleotides = [x for x in nucleotides if x != '\t']
        
        # Convert sequence to numpy array for model prediction
        sequence_vector = np.array([nucleotides])
        
        # Make prediction
        prediction = model.predict(sequence_vector)
        return jsonify({'class': str(prediction[0])})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(debug=True)
