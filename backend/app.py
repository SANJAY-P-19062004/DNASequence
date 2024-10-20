from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import pandas as pd
import joblib

app = Flask(__name__)
CORS(app)

# URL to fetch dataset from
model = joblib.load('model1.pkl') 
DATASET_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/molecular-biology/promoter-gene-sequences/promoters.data"  # Replace this with the actual URL

# Function to fetch dataset from URL and set column names
def fetch_dataset():
    try:
        # Fetch the CSV data from the URL
        response = requests.get(DATASET_URL)
        response.raise_for_status()  # Raises an exception for a failed request

        # Convert the fetched CSV content into a pandas DataFrame
        from io import StringIO
        csv_content = StringIO(response.text)
        df = pd.read_csv(csv_content, names=['class', 'id', 'sequence'])  # Assign column names

        # Convert DataFrame to a list of dictionaries
        dataset = df.to_dict(orient='records')
        return dataset
    except requests.exceptions.RequestException as e:
        print(f"Error fetching dataset: {e}")
        return []

# Function to match a sequence with the dataset
def find_sequence(sequence, dataset):
    for entry in dataset:
        if entry['sequence'] == sequence:
            return entry
    return None

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    sequence = data.get('sequence', '')

    if len(sequence) != 57:
        return jsonify({'error': 'Sequence must be exactly 57 nucleotides long.'}), 400

    # Fetch the dataset from the URL
    dataset = fetch_dataset()

    if not dataset:
        return jsonify({'error': 'Could not fetch dataset.'}), 500

    # Find the sequence in the dataset
    result = find_sequence(sequence, dataset)

    if result:
        return jsonify({'class': result['class'], 'id': result['id']})
    else:
        return jsonify({'error': 'Sequence not found in the dataset.'}), 404

if __name__ == '__main__':
    app.run(debug=True)
