import pickle
import pandas as pd
model = None
try:
    with open("model/model.pkl", "rb") as f:
        model = pickle.load(f)
except Exception as e:
    print("Warning: failed to load model.pkl:", e)

MODEL_VERSION = "1.0.0"

def predict_output(user_input : dict):
    input_df = pd.DataFrame([user_input])
    prediction = model.predict(input_df)[0]
    return prediction