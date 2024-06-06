from flask import Blueprint, request, jsonify

def default():
    return jsonify({"message": "Hello, World!"})