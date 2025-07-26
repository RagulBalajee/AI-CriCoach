# scripts/predictor.py

import os
import pickle
from sklearn.linear_model import LogisticRegression

def train_model(df_features):
    X = df_features.drop(columns=['win'])
    y = df_features['win']

    model = LogisticRegression(max_iter=1000)
    model.fit(X, y)

    # Save the trained model
    os.makedirs("models", exist_ok=True)
    with open("models/win_pred.pkl", "wb") as f:
        pickle.dump(model, f)

def load_model():
    with open("models/win_pred.pkl", "rb") as f:
        return pickle.load(f)
