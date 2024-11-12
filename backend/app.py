from flask import Flask, jsonify, request
import joblib
import numpy as np

app = Flask(__name__)

# Load your pre-trained model
model = joblib.load('model1.pkl')

@app.route('/')
def home():
    return "Welcome to the Promoter Gene Sequence Classifier!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the sequence from the request
        data = request.get_json(force=True)
        sequence = data.get('sequence', '').lower()

        # Validate the input sequence length
        if len(sequence) != 57:
            return jsonify({'error': 'Sequence must be exactly 57 nucleotides long.'}), 400

        # Convert sequence to list of nucleotides
        nucleotides = list(sequence)
        
        # Ensure the input has no tabs and other unwanted characters
        nucleotides = [x for x in nucleotides if x != '\t']

        # Convert nucleotides into the format expected by your model
        sequence_vector = np.array([nucleotides])

        # Make the prediction
        prediction = model.predict(sequence_vector)

        # Assuming '+' is Promoter and '-' is Non-Promoter
        class_label = prediction[0]
        result = 'Promoter' if class_label == '+' else 'Non-Promoter'

        # Return a structured response
        return jsonify({
            'class': class_label,
            'id': data.get('id', 'Unknown'),  # Include an ID if available
            'message': f'Sequence classified as {result}.'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
