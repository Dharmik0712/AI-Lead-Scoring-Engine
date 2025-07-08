import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
import joblib

df = pd.read_csv("leads.csv")

drop_cols = ["lead_id", "name", "lead_created_at", "intent_score"]  
X = df.drop(columns=drop_cols, errors="ignore")
y = df["intent_score"]

X = pd.get_dummies(X)

X.columns = [col.replace('[', '').replace(']', '').replace('<', '').replace('>', '').replace(' ', '_') for col in X.columns]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = xgb.XGBRegressor(n_estimators=100, max_depth=5, learning_rate=0.1)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
auc = roc_auc_score((y_test > 0.5), y_pred)  
print(f"✅ AUC Score: {auc:.3f}")

joblib.dump(model, "lead_score_model.pkl")
X.columns.to_series().to_csv("feature_columns.csv", index=False)

print("✅ Model trained and saved.")