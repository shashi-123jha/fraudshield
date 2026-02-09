import jwt
import bcrypt
from datetime import datetime, timedelta
from flask import request, jsonify
from functools import wraps
from db import users

SECRET_KEY = "fraudshield_secret"

def signup():
    data = request.json
    hashed = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt())

    if users.find_one({"email": data["email"]}):
        return jsonify({"error": "User already exists"}), 400

    users.insert_one({
        "email": data["email"],
        "password": hashed,
        "role": data.get("role", "user")
    })

    return jsonify({"message": "Signup successful"})

def login():
    data = request.json
    user = users.find_one({"email": data["email"]})

    if not user or not bcrypt.checkpw(data["password"].encode(), user["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    token = jwt.encode({
        "email": user["email"],
        "role": user["role"],
        "exp": datetime.utcnow() + timedelta(hours=2)
    }, SECRET_KEY, algorithm="HS256")

    return jsonify({"token": token})

def token_required(role=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = request.headers.get("Authorization")
            if not token:
                return jsonify({"error": "Token missing"}), 401

            try:
                data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                if role and data["role"] != role:
                    return jsonify({"error": "Access denied"}), 403
            except:
                return jsonify({"error": "Invalid token"}), 401

            return f(*args, **kwargs)
        return wrapper
    return decorator
