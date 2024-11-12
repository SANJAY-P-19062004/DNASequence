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

    data = request.json
    sequence = data.get('sequence', '').lower()  # Convert sequence to lowercase

    # Ensure sequence length is correct
    if len(sequence) != 57:
        return jsonify({'error': 'Sequence must be exactly 57 nucleotides long.'}), 400

    # Fetch dataset to compare input sequence
    dataset = fetch_dataset()
    if not dataset:
        return jsonify({'error': 'Could not fetch dataset.'}), 500

    # Check if sequence exists in dataset
    matched_entry = next((entry for entry in dataset if entry['sequence'] == sequence), None)
    
    if matched_entry:
        # Sequence is found in the dataset
        return jsonify({
            'class': matched_entry['class'],
            'id': matched_entry['id'],
            'message': 'Sequence found in dataset.'
        })
    else:
        # Sequence is not found in the dataset, proceed with model prediction
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
        feature_vector = pd.DataFrame(feature_vector).values.flatten().reshape(1, -1)

        # Predict using the loaded model
        prediction = model.predict(feature_vector)

        # Return the prediction result
        if prediction[0] == 1:
            result = {'class': 'Promoter', 'message': 'This sequence is classified as Promoter.'}
        else:
            result = {'class': 'Non-Promoter', 'message': 'This sequence is classified as Non-Promoter.'}
        
        return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
