import joblib
import os
import numpy as np
import pandas as pd
import warnings
import services.data as data
warnings.simplefilter("ignore", category=UserWarning)


def round_to_3dp(array):
    return np.round(array, 3)


def get_columns():
    try:
        features_str = os.getenv('FEATURES')
        if features_str:
            features = features_str.split(',')
            return features
    except Exception as e:
        print(f"Error: {e}")
        return None


def select_features(json_data):
    return {key: json_data[key] for key in get_columns()}


def predict(data):
    try:
        scaler = joblib.load("data/scaler.pkl")
        model = joblib.load("data/xgb_model.pkl")

        df = pd.DataFrame([select_features(data)])

        for col in get_columns():
            df[col] = df[col].apply(lambda x: np.log(x) if x > 0 else 0)

        input_scaled = scaler.transform(df.head(1))

        _input = round_to_3dp(input_scaled)

        prediction = model.predict(_input.tolist())

        return prediction.tolist()[0]
    except Exception as e:
        print(f"Error: {e}")
        return None


def detect(address):
    try:
        json_data = data.get_data(address)
        if not json_data:
            return None
        return predict(json_data)
    except Exception as e:
        print(f"Error: {e}")
        return None
