import os
from datetime import datetime
from typing import ClassVar, Dict, Type, Union

import pytz
from dotenv import load_dotenv
from pytz.tzinfo import BaseTzInfo

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config:
    SECRET_KEY: Union[str, bytes] = os.environ.get("SECRET_KEY") or os.urandom(24)
    SQLALCHEMY_DATABASE_URI: str = f"sqlite:///{os.path.join(basedir, 'mails.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    DEBUG: bool = False
    TESTING: bool = False

    TIMEZONE: ClassVar[BaseTzInfo] = pytz.timezone("Asia/Tokyo")

    @staticmethod
    def now_jst() -> datetime:
        """現在のJST時刻を返す"""
        return datetime.now(Config.TIMEZONE)


class DevelopmentConfig(Config):
    SECRET_KEY: Union[str, bytes] = os.environ.get("SECRET_KEY") or os.urandom(24)
    DEBUG: bool = True


class TestingConfig(Config):
    SECRET_KEY: Union[str, bytes] = os.environ.get("SECRET_KEY") or os.urandom(24)
    TESTING: bool = True
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///:memory:"


class StagingConfig(Config):
    SECRET_KEY: Union[str, bytes] = os.environ.get("SECRET_KEY") or os.urandom(24)


class ProductionConfig(Config):
    SECRET_KEY: Union[str, bytes] = os.environ.get("SECRET_KEY") or os.urandom(24)


config: Dict[str, Type[Config]] = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "staging": StagingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
