import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import config

db: SQLAlchemy = SQLAlchemy()


def create_app(config_name: str) -> Flask:
    """アプリ作成用ファクトリ"""
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
        from . import routes  # noqa: F401

    db.init_app(app)

    return app
