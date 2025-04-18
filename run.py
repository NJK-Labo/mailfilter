import os

from dotenv import load_dotenv
from flask import Flask

from app import create_app

basedir: str = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))

config_name: str = os.getenv("FLASK_CONFIG", "default")
app: Flask = create_app(config_name)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
