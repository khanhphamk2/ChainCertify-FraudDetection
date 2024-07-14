from flask import Flask, request, jsonify
import services.home as home
import services.model as model
import services.data as data

app = Flask(__name__)


@app.route("/", methods=['GET'])
def hello_world():
    return home.default()


@app.route('/api/data/<address>', methods=['GET'])
def get_data(address):
    return data.get_data(address)


@app.route('/api/predict/', methods=['POST'])
def predict():
    json_data = request.get_json()
    return jsonify(model.predict(json_data))


@app.route('/api/detect/<address>', methods=['GET'])
def detect(address):
    try:
        return jsonify(model.detect(address))
    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {e}"


if __name__ == '__main__':
    app.run(debug=True)
