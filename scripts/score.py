import json
import os
import joblib
import numpy as np

model = None

def init():
    global model

    model_dir = os.getenv("AZUREML_MODEL_DIR")
    print("AZUREML_MODEL_DIR =", model_dir)

    if model_dir is None:
        raise ValueError("AZUREML_MODEL_DIR is not set")

    found_files = []

    for root, dirs, files in os.walk(model_dir):
        print("Checking:", root, files)
        for file in files:
            found_files.append(os.path.join(root, file))
            if file.endswith(".pkl"):
                model_path = os.path.join(root, file)
                print("Loading model from:", model_path)
                model = joblib.load(model_path)
                print("Model loaded successfully")
                return

    raise FileNotFoundError("No .pkl file found. Files seen: " + str(found_files))

def run(raw_data):
    try:
        data = json.loads(raw_data)
        inputs = np.array(data["data"])
        preds = model.predict(inputs)
        return {"predictions": preds.tolist()}
    except Exception as e:
        return {"error": str(e)}
