import json
import os
import joblib
import pandas as pd

model = None

def init():
    global model
    model_path = os.path.join(os.getenv("AZUREML_MODEL_DIR"), "model.pkl")
    model = joblib.load(model_path)

def run(raw_data):
    try:
        data = json.loads(raw_data)
        df = pd.DataFrame(data["data"])
        preds = model.predict(df)
        return {"predictions": preds.tolist()}
    except Exception as e:
        return {"error": str(e)}