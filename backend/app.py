from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This enables CORS for all domains, ensure it is enabled for your domain if necessary

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the sequence from the request body
        data = request.get_json()
        sequence = data.get('sequence')

        if not sequence:
            return jsonify({'error': 'No sequence provided'}), 400

        # Ensure the sequence length is 57 (as per your request)
        if len(sequence) != 57:
            return jsonify({'error': 'Sequence must be exactly 57 characters long'}), 400

        # For the sake of example, let's mock the prediction process
        # Replace this with actual model prediction logic
        prediction = '+'  # Change this based on your model's logic
        return jsonify({'prediction': prediction})

    except Exception as e:
        # If any error occurs, log it and return a 500 error
        print(f"Error: {str(e)}")
        return jsonify({'error': 'An internal error occurred'}), 500

if __name__ == "__main__":
    app.run(debug=True)
