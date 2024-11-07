from flask import Flask, request, jsonify
import pandas as pd
import requests
from io import StringIO

app = Flask(__name__)

# URL of your dataset (replace with the actual URL)
dataset_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/molecular-biology/promoter-gene-sequences/promoters.data"

def load_dataset():
    # Fetch the dataset from the URL
    response = requests.get(dataset_url)
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Load the dataset into a pandas DataFrame
        data = StringIO(response.text)
        df = pd.read_csv(data)
        return df
    else:
        return None

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the sequence from the request
        data = request.get_json()
        sequence = data.get('sequence')

        if not sequence:
            return jsonify({'error': 'No sequence provided'}), 400
        
        # Load the dataset from the URL
        df = load_dataset()
        
        if df is None:
            return jsonify({'error': 'Failed to load the dataset'}), 500
        
        # Search for the sequence in the dataset
        match = df[df['sequence'] == sequence]

        # If the sequence is found
        if not match.empty:
            # Get the class (either '+' or '-')
            prediction_class = match.iloc[0]['class']
            
            if prediction_class == '+':
                prediction = 'Promoter'
            else:
                prediction = 'Non-Promoter'
            
            return jsonify({'class': prediction_class, 'prediction': prediction}), 200
        
        # If the sequence is not found
        return jsonify({'error': 'Sequence not found in the dataset'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
