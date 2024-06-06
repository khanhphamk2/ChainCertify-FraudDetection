from flask import Blueprint, request, jsonify
import numpy as np
import src.services.model as model
import src.services.data as data

model_bp = Blueprint('model', __name__)


@model_bp.route('/api/predict', methods=['POST'])
def predict():
    return model.predict(list(request.json.values()))


@model.route('/api/prediction', methods=['POST'])
def prediction():
    try:
        arr = data.get_txs_by_address(request.json['address'])
        return model.predict(arr)
    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {e}"
