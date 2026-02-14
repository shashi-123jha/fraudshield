import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib
import random

# ===============================
# Generate Synthetic Dataset
# ===============================

data = []

for _ in range(5000):

    amount = random.randint(100, 50000)
    transaction_type = random.randint(0, 4)
    location = random.randint(0, 2)

    # Fraud logic (simple realistic pattern)
    fraud = 0

    if amount > 20000:
        fraud = 1

    if transaction_type == 4:  # Crypto
        fraud = 1

    if location == 2 and amount > 10000:
        fraud = 1

    data.append([amount, transaction_type, location, fraud])

df = pd.DataFrame(data, columns=[
    "amount",
    "transaction_type",
    "location",
    "fraud"
])

# ===============================
# Train Model
# ===============================

X = df[["amount", "transaction_type", "location"]]
y = df["fraud"]

model = RandomForestClassifier(n_estimators=100)
model.fit(X, y)

# ===============================
# Save Model
# ===============================

joblib.dump(model, "fraud_model.pkl")

print("✅ Model trained and saved successfully!")
