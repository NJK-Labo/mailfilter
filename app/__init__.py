import logging

from flask import Flask

from config import config


def create_app(config_name: str) -> Flask:
    app: Flask = Flask(__name__)
    app.config.from_object(config[config_name])

    # ロガーの設定
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # ルートのインポート
    with app.app_context():
        from . import routes

    return app
