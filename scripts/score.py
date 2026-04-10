import json
import os
import joblib
import numpy as np

model = None

def init():
    global model

    model_dir = os.getenv("AZUREML_MODEL_DIR")
    print("AZUREML_MODEL_DIR:", model_dir)

    for root, dirs, files in os.walk(model_dir):
        print("ROOT:", root)
        print("FILES:", files)
        for file in files:
            if file.endswith(".pkl"):
                model_path = os.path.join(root, file)
                print("Loading model from:", model_path)
                model = joblib.load(model_path)
                print("Model loaded successfully")
                return

    raise FileNotFoundError("No .pkl model file found inside AZUREML_MODEL_DIR")

def run(raw_data):
    data = json.loads(raw_data)
    inputs = np.array(data["data"])
    preds = model.predict(inputs)
    return {"predictions": preds.tolist()}
