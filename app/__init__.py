from flask import Flask

from config import config


def create_app(config_name: str) -> Flask:
    app: Flask = Flask(__name__)
    app.config.from_object(config[config_name])

    with app.app_context():
        from . import routes

    return app
