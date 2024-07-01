from flask import jsonify

def default():
    return jsonify({"message": "Hello, World!"})