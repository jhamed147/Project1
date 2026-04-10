import json
import joblib
import numpy as np
import os

def init():
    global model
    model_path = os.path.join(os.getenv("AZUREML_MODEL_DIR"), "ames_rf_model.pkl")
    model = joblib.load(model_path)

def run(raw_data):
    data = json.loads(raw_data)
    inputs = data["data"]
    preds = model.predict(np.array(inputs))
    return {"predictions": preds.tolist()}
