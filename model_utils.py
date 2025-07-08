import joblib
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder

model = joblib.load("lead_score_model.pkl")

try:
    import json
    with open("feature_columns.json") as f:
        feature_cols = json.load(f)
except:
    feature_cols = pd.read_csv("feature_columns.csv", header=None).squeeze().tolist()

def preprocess(lead: dict) -> pd.DataFrame:
    df = pd.DataFrame([lead])
    df = pd.get_dummies(df)
    for col in feature_cols:
        if col not in df.columns:
            df[col] = 0
    df = df[feature_cols]
    return df

def predict(lead: dict) -> float:
    X = preprocess(lead)
    score = model.predict(X)[0]
    return float(round(score, 4)) 