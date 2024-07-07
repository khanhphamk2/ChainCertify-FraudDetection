from flask import Flask, request, jsonify
import services.home as home
import services.model as model
import services.data as data

app = Flask(__name__)


@app.route('/api/data', methods=['GET'])
def get_data():
    address = request.get_json().get("address")
    return data.get_data(address)


@app.route("/", methods=['GET'])
def hello_world():
    return home.default()


@app.route('/api/predict', methods=['POST'])
def predict():
    res = request.get_json()
    return jsonify(model.predict(res))


@app.route('/api/prediction', methods=['POST'])
def prediction():
    try:
        arr = data.get_txs_by_address(request.get_json().get("address"))
        return model.predict(arr)
    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {e}"


if __name__ == '__main__':
    app.run(debug=True)
