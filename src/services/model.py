import joblib
import numpy as np
import warnings
from flask import jsonify
import src.services.data as data


def round_to_3dp(array):
    return np.round(array, 3)


def predict(data):
    with warnings.catch_warnings():
        try:
            warnings.simplefilter("ignore", category=UserWarning)

            scaler = joblib.load("app/data/scaler.pkl")
            model = joblib.load("app/data/xgb_model.pkl")

            input_array = np.array(data)

            result_array = np.where(input_array > 0, np.log(input_array), 0)

            input_scaled = scaler.transform(result_array)

            _input = round_to_3dp(input_scaled)

            prediction = model.predict(_input)

            return jsonify(prediction.tolist())
        except Exception as e:
            print(f"Error: {e}")
            return None


def get_stats(address):
    try:
        sample = data.get_data(address)
        if not sample:
            return None
        return predict(sample)
    except Exception as e:
        print(f"Error: {e}")
        return None
