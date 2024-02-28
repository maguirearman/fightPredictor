from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/predict-fight', methods=['POST'])
def predict_fight():
    # Receive selected parameters from the frontend
    data = request.json
    weight_class = data['weight_class']
    fighter_ids = [data['fighter1'], data['fighter2']]

    # Logic to fetch fight IDs based on weight class and fighter IDs
    # This is where you would interact with your database or any other data source

    # Dummy prediction using placeholders
    predicted_winner = 'Fighter 1' if weight_class == 'Flyweight' else 'Fighter 2'

    # Return the predicted winner to the frontend
    return jsonify({'predicted_winner': predicted_winner})

if __name__ == '__main__':
    app.run(debug=True)
