from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import pandas as pd
import joblib

app = Flask(__name__)
CORS(app)

model = joblib.load('model1.pkl')
DATASET_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/molecular-biology/promoter-gene-sequences/promoters.data"

def fetch_dataset():
    try:
        response = requests.get(DATASET_URL)
        response.raise_for_status()
        from io import StringIO
        csv_content = StringIO(response.text)
        df = pd.read_csv(csv_content, names=['class', 'id', 'sequence'])
        return df.to_dict(orient='records')
    except requests.RequestException as e:
        print(f"Error fetching dataset: {e}")
        return []

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

    dataset = fetch_dataset()
    if not dataset:
        return jsonify({'error': 'Could not fetch dataset.'}), 500

    result = find_sequence(sequence, dataset)
    if result:
        return jsonify({'class': result['class'], 'id': result['id']})
    else:
        return jsonify({'error': 'Sequence not found in the dataset.'}), 404

if __name__ == '__main__':
    app.run(debug=True)
