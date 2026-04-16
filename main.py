from fastapi import FastAPI
import mlflow.sklearn
import pandas as pd

app = FastAPI()

# This is the 'Showroom' path
model_uri = "models:/Lloyds_Churn_Production_Project/1"

try:
    model = mlflow.sklearn.load_model(model_uri)
    print("SUCCESS: Lloyds Model is now LIVE in FastAPI!")
except Exception as e:
    print(f"STILL LOADING: {e}")

@app.get("/")
def home():
    return {"status": "Online"}

@app.post("/predict")
def predict(data: dict):
    df = pd.DataFrame([data])
    prediction = model.predict(df)[0]
    return {"prediction": "Churn" if prediction == 1 else "Stay"}