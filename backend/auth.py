import jwt
import bcrypt
from datetime import datetime, timedelta
from flask import request, jsonify
from functools import wraps
from db import users

# 🔐 Secret key (move to .env in production)
SECRET_KEY = "fraudshield_secret"

# =========================
# SIGNUP
# =========================
def signup():
    data = request.json

    # Basic validation
    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Email and password required"}), 400

    # Check existing user
    if users.find_one({"email": data["email"]}):
        return jsonify({"error": "User already exists"}), 400

    # Hash password
    hashed_password = bcrypt.hashpw(
        data["password"].encode("utf-8"),
        bcrypt.gensalt()
    )

    # Insert user
    users.insert_one({
        "email": data["email"],
        "password": hashed_password,
        "role": data.get("role", "user"),
        "created_at": datetime.utcnow()
    })

    return jsonify({"message": "Signup successful"}), 201


# =========================
# LOGIN
# =========================
def login():
    data = request.json

    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Email and password required"}), 400

    user = users.find_one({"email": data["email"]})
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    # Check password
    if not bcrypt.checkpw(
        data["password"].encode("utf-8"),
        user["password"]
    ):
        return jsonify({"error": "Invalid credentials"}), 401

    # Create JWT token
    token = jwt.encode(
        {
            "email": user["email"],
            "role": user["role"],
            "exp": datetime.utcnow() + timedelta(hours=2)
        },
        SECRET_KEY,
        algorithm="HS256"
    )

    return jsonify({
        "token": token,
        "expires_in": "2 hours"
    }), 200


# =========================
# TOKEN REQUIRED DECORATOR
# =========================
def token_required(role=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get("Authorization")

            # Check header format
            if not auth_header or not auth_header.startswith("Bearer "):
                return jsonify({"error": "Authorization token missing"}), 401

            token = auth_header.split(" ")[1]

            try:
                decoded = jwt.decode(
                    token,
                    SECRET_KEY,
                    algorithms=["HS256"]
                )

                # Role-based access control
                if role and decoded.get("role") != role:
                    return jsonify({"error": "Access denied"}), 403

                # Attach user info to request (optional but useful)
                request.user = decoded

            except jwt.ExpiredSignatureError:
                return jsonify({"error": "Token expired"}), 401
            except jwt.InvalidTokenError:
                return jsonify({"error": "Invalid token"}), 401
            except Exception:
                return jsonify({"error": "Authentication failed"}), 401

            return f(*args, **kwargs)
        return wrapper
    return decorator
