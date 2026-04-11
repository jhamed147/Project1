import json
import os
import joblib
import numpy as np

model = None

def init():
    global model

    model_dir = os.getenv("AZUREML_MODEL_DIR")

    if model_dir is None:
        raise ValueError("AZUREML_MODEL_DIR is not set")

    for root, dirs, files in os.walk(model_dir):
        for file in files:
            if file.endswith(".pkl"):
                model_path = os.path.join(root, file)
                model = joblib.load(model_path)
                return

    raise FileNotFoundError("No .pkl file found inside AZUREML_MODEL_DIR")

def run(raw_data):
    data = json.loads(raw_data)
    inputs = np.array(data["data"])
    preds = model.predict(inputs)
    return {"predictions": preds.tolist()}
