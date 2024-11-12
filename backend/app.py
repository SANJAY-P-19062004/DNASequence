from flask import Flask, jsonify, request
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Initialize Flask app
app = Flask(__name__)

# Load the saved model
model = joblib.load('model1.pkl')

# Optionally, load a scaler if you're using one in preprocessing (you can adjust based on your model preprocessing steps)
# scaler = joblib.load('scaler.pkl')  # Uncomment if you're using a scaler

@app.route('/')
def home():
    return "Welcome to the Promoter Gene Sequence Classifier!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get JSON data from request
        data = request.get_json(force=True)
        
        # Assume the input data has the gene sequence in a field named 'sequence'
        sequence = data['sequence']
        
        # Process the sequence to match the model's expected input
        # Convert sequence to list of nucleotides
        nucleotides = list(sequence)
        nucleotides = [x for x in nucleotides if x != '\t']
        
        # Convert nucleotides into a format suitable for your model
        # Create a DataFrame for model prediction (ensure you encode or transform data as needed)
        # Example transformation step, customize based on your dataset's feature encoding
        sequence_vector = np.array([nucleotides])  # You may need more preprocessing depending on your model
        
        # If you used scaling, apply the scaler here
        # sequence_vector = scaler.transform(sequence_vector)  # Uncomment if scaler was used

        # Make the prediction
        prediction = model.predict(sequence_vector)
        
        # Return the prediction in a JSON format
        return jsonify({'prediction': str(prediction[0])})  # Assuming binary classes (+ or -)
    
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(debug=True)
