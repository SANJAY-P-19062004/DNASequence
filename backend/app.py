from flask import Flask, jsonify, request
import joblib
import numpy as np

app = Flask(__name__)

# Load your pre-trained model
try:
    model = joblib.load('model1.pkl')
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")

@app.route('/')
def home():
    return "Welcome to the Promoter Gene Sequence Classifier!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the sequence from the request body
        data = request.get_json(force=True)
        if 'sequence' not in data:
            return jsonify({'error': 'No sequence field found in the request'}), 400

        sequence = data['sequence'].lower()

        # Validate sequence length
        if len(sequence) != 57:
            return jsonify({'error': 'Sequence must be exactly 57 nucleotides long.'}), 400

        # Convert sequence to list of nucleotides
        nucleotides = list(sequence)

        # Prepare input for model (convert to numpy array with shape (1, 57))
        sequence_vector = np.array([nucleotides])

        # Make prediction
        try:
            prediction = model.predict(sequence_vector)
        except Exception as model_error:
            print(f"Model prediction error: {model_error}")
            return jsonify({'error': 'Error occurred during model prediction.'}), 500

        # Interpret the prediction
        class_label = prediction[0]
        result = 'Promoter' if class_label == '+' else 'Non-Promoter'

        return jsonify({
            'class': class_label,
            'id': data.get('id', 'N/A'),
            'message': f'Sequence classified as {result}.'
        })
    
    except Exception as e:
        print(f"Server error: {e}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == "__main__":
    app.run(debug=True)
