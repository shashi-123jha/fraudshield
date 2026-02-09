from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import joblib

from db import transactions
from auth import signup, login, token_required

app = Flask(__name__)
CORS(app)

model = joblib.load("fraud_model.pkl")

@app.route("/")
def home():
    return "FraudShield Backend Running"

# AUTH
@app.route("/signup", methods=["POST"])
def signup_route():
    return signup()

@app.route("/login", methods=["POST"])
def login_route():
    return login()

# PREDICT (USER)
@app.route("/predict", methods=["POST"])
@token_required(role="user")
def predict():
    data = request.json

    features = [
        data["amount"],
        data["transaction_type"],
        data["location"],
        data["time"]
    ]

    prediction = model.predict([features])[0]
    result = "Fraudulent" if prediction == 1 else "Legitimate"

    transactions.insert_one({
        **data,
        "prediction": result,
        "created_at": datetime.utcnow()
    })

    return jsonify({"prediction": result})

# ADMIN DASHBOARD
@app.route("/admin/transactions", methods=["GET"])
@token_required(role="admin")
def admin_transactions():
    data = list(transactions.find({}, {"_id": 0}))
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
