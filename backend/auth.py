import jwt
import datetime
from functools import wraps
from flask import request, jsonify
from db import users_collection

SECRET_KEY = "supersecretkey"


# ================= SIGNUP =================
def signup():
    data = request.json

    if users_collection.find_one({"email": data["email"]}):
        return jsonify({"error": "User already exists"}), 400

    users_collection.insert_one({
        "name": data["name"],
        "email": data["email"],
        "password": data["password"],
        "role": data["role"]
    })

    return jsonify({"message": "Signup successful"}), 201


# ================= LOGIN =================
def login():
    data = request.json
    user = users_collection.find_one({"email": data["email"]})

    if not user or user["password"] != data["password"]:
        return jsonify({"error": "Invalid credentials"}), 401

    token = jwt.encode({
        "email": user["email"],
        "role": user["role"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=3)
    }, SECRET_KEY, algorithm="HS256")

    return jsonify({"token": token})


# ================= TOKEN REQUIRED =================
def token_required(role=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get("Authorization")

            if not auth_header:
                return jsonify({"error": "Authorization token missing"}), 401

            try:
                token = auth_header.split(" ")[1]
                decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

                if role and decoded["role"] != role:
                    return jsonify({"error": "Access denied"}), 403

            except:
                return jsonify({"error": "Invalid token"}), 401

            return f(*args, **kwargs)

        return wrapper
    return decorator
