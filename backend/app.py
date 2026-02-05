from flask import Flask, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

# Load ML model
with open("fraud_model.pkl", "rb") as f:
    model = pickle.load(f)

@app.route('/')
def home():
    return "FraudShield API is Running"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json

    amount = data['amount']
    location = data['location']
    tx_type = data['type']

    features = np.array([[amount, location, tx_type]])
    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0][1]

    result = "Fraudulent" if prediction == 1 else "Legitimate"

    return jsonify({
        "prediction": result,
        "confidence": round(probability * 100, 2)
    })

if __name__ == "__main__":
    app.run(debug=True)
