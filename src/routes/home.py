from flask import Blueprint, request, jsonify
import src.services.home as home

home_bp = Blueprint('home', __name__)


@home_bp.route("/", methods=['GET'])
def hello_world():
    return home.default()
