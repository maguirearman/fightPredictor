from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/predict', methods=['OPTIONS', 'POST'])
def predict_fight():
    if request.method == 'OPTIONS':
        response = jsonify({'message': 'Preflight request accepted.'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', '*')
        response.headers.add('Access-Control-Allow-Methods', '*')
        return response

    if request.method == 'POST':
        # Receive selected parameters from the frontend
        data = request.json
        weight_class = data['weightClass']
        fighter1 = data['fighter1']
        fighter2 = data['fighter2']

        # Dummy prediction using placeholders
        predicted_winner = 'Fighter 1' if weight_class == 'Flyweight' else 'Fighter 2'

        response = jsonify({'predicted_winner': predicted_winner})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

if __name__ == '__main__':
    app.run(debug=True)
