import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pickle

# Sample transaction dataset
data = {
    'amount': [100, 2000, 150, 5000, 60, 7000, 120, 9000],
    'location': [0, 1, 0, 1, 0, 1, 0, 1],  # 0 = Local, 1 = International
    'type': [0, 1, 0, 1, 0, 1, 0, 1],      # 0 = Normal, 1 = Suspicious
    'fraud': [0, 1, 0, 1, 0, 1, 0, 1]
}

df = pd.DataFrame(data)

X = df[['amount', 'location', 'type']]
y = df['fraud']

model = LogisticRegression()
model.fit(X, y)

# Save trained model
with open("fraud_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Fraud Detection Model Trained & Saved")
