from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import joblib

from db import transactions
from auth import token_required
from routes.auth_routes import auth_routes

app = Flask(__name__)
CORS(app)

# Load ML model
model = joblib.load("fraud_model.pkl")

@app.route("/")
def home():
    return "FraudShield Backend Running"

# Register Auth Blueprint
app.register_blueprint(auth_routes, url_prefix="/api/auth")

# ==========================
# USER PREDICTION ROUTE
# ==========================
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

# ==========================
# ADMIN DASHBOARD
# ==========================
@app.route("/admin/transactions", methods=["GET"])
@token_required(role="admin")
def admin_transactions():
    data = list(transactions.find({}, {"_id": 0}))
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
