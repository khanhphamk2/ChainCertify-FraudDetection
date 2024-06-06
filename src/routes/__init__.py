from flask import Blueprint
from .home import home_bp
from .model import model_bp
from .data import data_bp


def init_routes(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(data_bp)
    app.register_blueprint(model_bp)
