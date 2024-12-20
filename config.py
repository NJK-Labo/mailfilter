import os
from datetime import datetime
from typing import ClassVar, Dict, Type

import pytz
from dotenv import load_dotenv
from pytz.tzinfo import BaseTzInfo


class ConfigError(Exception):
    """設定関連のエラー"""

    pass


basedir: str = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config:
    SECRET_KEY: str | None = os.environ.get("SECRET_KEY")
    if SECRET_KEY is None:
        raise ConfigError("環境変数にSECRET_KEYが登録されていません")

    SQLALCHEMY_DATABASE_URI: str | None = os.environ.get("DATABASE_URL")
    if SQLALCHEMY_DATABASE_URI is None:
        raise ConfigError("環境変数にDATABASE_URLが登録されていません")

    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    DEBUG: bool = False
    TESTING: bool = False

    TIMEZONE: ClassVar[BaseTzInfo] = pytz.timezone("Asia/Tokyo")

    @staticmethod
    def now_jst() -> datetime:
        """現在のJST時刻を返す"""
        return datetime.now(Config.TIMEZONE)


class DevelopmentConfig(Config):
    DEBUG: bool = True


class TestingConfig(Config):
    TESTING: bool = True
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///:memory:"


class StagingConfig(Config):
    pass


class ProductionConfig(Config):
    pass


config: Dict[str, Type[Config]] = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "staging": StagingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
