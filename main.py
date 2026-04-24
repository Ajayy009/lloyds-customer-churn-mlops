from fastapi import FastAPI
import pandas as pd
import joblib
import mlflow
import os

app = FastAPI()

# 1. Setup Direct Connection to the Shared Volume
MLFLOW_TRACKING_URI = "sqlite:////mlflow_data/mlflow.db"
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

try:
    # Load from MLflow registry
    model_uri = "models:/Lloyds_Churn_Production_Project_V2/1"
    model = mlflow.pyfunc.load_model(model_uri)
    print("SUCCESS: Loaded from MLflow Registry!")
    model_source = "MLflow Registry"
except Exception as e:
    print(f"MLflow failed ({e}). Using pickle...")
    model = joblib.load("model.pkl")
    model_source = "Local Pickle (Backup)"

@app.get("/")
def home():
    return {"status": "Online", "mode": "Shared-Volume-Access", "brain_source": model_source}

@app.post("/predict")
def predict(data: dict):
    df = pd.DataFrame([data])
    prediction = model.predict(df)[0]
    return {
        "prediction": "Churn" if prediction == 1 else "Stay",
        "model_used": model_source
    }