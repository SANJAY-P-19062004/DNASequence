from flask import Flask, request, jsonify
import time

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Simulate a delay for debugging
        time.sleep(2)

        # Get the sequence from the request body
        data = request.get_json()
        sequence = data.get('sequence')

        if not sequence or len(sequence) != 57:
            return jsonify({'error': 'Invalid sequence'}), 400

        # Perform your sequence classification logic here
        # For example, let's pretend we are making a prediction
        prediction = '+'  # or '-' based on your model

        return jsonify({'prediction': prediction})

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': 'An error occurred'}), 500

if __name__ == "__main__":
    app.run(debug=True)
