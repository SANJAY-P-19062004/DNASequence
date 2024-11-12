from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import pandas as pd
import joblib
import os

app = Flask(__name__)
CORS(app)

# Load pre-trained model
model_path = 'model1.pkl'
if os.path.exists(model_path):
    model = joblib.load(model_path)
else:
    model = None  # Handle case if model is missing

# Dataset URL for fetching promoter sequences
DATASET_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/molecular-biology/promoter-gene-sequences/promoters.data"

def fetch_dataset():
    try:
        response = requests.get(DATASET_URL)
        response.raise_for_status()  # Ensure the response was successful
        
        # Parse UCI dataset format
        from io import StringIO
        csv_content = StringIO(response.text)
        df = pd.read_csv(csv_content, header=None, names=['class', 'id', 'sequence'])
        
        # Ensure the dataset contains the expected columns
        if 'class' not in df.columns or 'id' not in df.columns or 'sequence' not in df.columns:
            raise ValueError("Dataset format is incorrect, expected columns: 'class', 'id', 'sequence'")
        
        return df.to_dict(orient='records')
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching dataset: {e}")
        return []
    except ValueError as e:
        print(f"Dataset format error: {e}")
        return []

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model not available'}), 500

    # Get the sequence from the request
    data = request.json
    sequence = data.get('sequence', '')

    # Ensure sequence length is correct (57 nucleotides expected in your dataset)
    if len(sequence) != 57:
        return jsonify({'error': 'Sequence must be exactly 57 nucleotides long.'}), 400

    # Prepare the sequence for prediction
    nucleotides = list(sequence)
    nucleotides = [x for x in nucleotides if x != '\t']  # Remove any unwanted characters
    
    # Create a feature vector for the sequence (this is based on your preprocessing)
    feature_vector = []

    for nucleotide in nucleotides:
        if nucleotide == 'a':
            feature_vector.append([1, 0, 0, 0])  # A: [1, 0, 0, 0]
        elif nucleotide == 'c':
            feature_vector.append([0, 1, 0, 0])  # C: [0, 1, 0, 0]
        elif nucleotide == 'g':
            feature_vector.append([0, 0, 1, 0])  # G: [0, 0, 1, 0]
        elif nucleotide == 't':
            feature_vector.append([0, 0, 0, 1])  # T: [0, 0, 0, 1]

    # Flatten the list to create the final input feature vector
    feature_vector = np.array(feature_vector).flatten().reshape(1, -1)

    # Predict using the loaded model
    prediction = model.predict(feature_vector)

    # Create the response based on the prediction
    result = {
        'class': 'Promoter' if prediction[0] == 1 else 'Non-Promoter',
        'id': 'S10',  # Just for testing, replace with your actual logic for 'id'
        'message': 'Sequence found in dataset.'
    }

    # Debugging print
    print("Response being sent to frontend:", result)

    # Return the prediction result
    return jsonify(result)
