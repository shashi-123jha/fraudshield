from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import joblib

from db import transactions_collection
from auth import token_required
from routes.auth_routes import auth_routes

app = Flask(__name__)
CORS(app)

model = joblib.load("fraud_model.pkl")


@app.route("/")
def home():
    return "FraudShield Backend Running"


# Register auth blueprint
app.register_blueprint(auth_routes, url_prefix="/api/auth")


# ==========================
# FRAUD PREDICTION ROUTE
# ==========================
@app.route("/predict", methods=["POST"])
@token_required(role="user")
def predict():

    data = request.json

    try:
        amount = float(data["amount"])
        transaction_type = int(data["transaction_type"])
        location = int(data["location"])
        device = int(data["device"])
        failed_attempts = int(data["failedAttempts"])
        time = int(data["time"])
    except:
        return jsonify({"error": "Invalid or missing fields"}), 400

    # ---- ML Prediction ----
    features = [amount, transaction_type, location]
    prediction = model.predict([features])[0]
    ml_result = "Fraudulent" if prediction == 1 else "Legitimate"

    # ---- Behavioral Risk Score ----
    risk_score = 0

    if amount > 10000:
        risk_score += 2

    if transaction_type >= 4:
        risk_score += 2
    else:
        risk_score += 1

    if location == 3:
        risk_score += 2

    if device == 2:
        risk_score += 2

    if failed_attempts > 2:
        risk_score += 2

    if time == 2:
        risk_score += 1

    # ---- Final Decision ----
    final_result = ml_result
    if risk_score >= 6:
        final_result = "Fraudulent (High Risk Behavior)"

    # ---- Save Transaction ----
    transactions_collection.insert_one({
        "amount": amount,
        "transaction_type": transaction_type,
        "location": location,
        "device": device,
        "failed_attempts": failed_attempts,
        "time": time,
        "ml_prediction": ml_result,
        "risk_score": risk_score,
        "final_result": final_result,
        "created_at": datetime.utcnow()
    })

    return jsonify({
        "ml_prediction": ml_result,
        "risk_score": risk_score,
        "final_result": final_result
    })


# ==========================
# ADMIN DASHBOARD
# ==========================
@app.route("/admin/transactions", methods=["GET"])
@token_required(role="admin")
def admin_transactions():
    data = list(transactions_collection.find({}, {"_id": 0}))
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
