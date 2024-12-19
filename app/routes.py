import logging

from flask import current_app as app
from flask import render_template
from werkzeug.exceptions import InternalServerError, NotFound

logger = logging.getLogger(__name__)


@app.route("/")
def index() -> str:
    """トップ画面"""
    return render_template("index.html")


@app.route("/contact-emails")
def list_contact_emails() -> str:
    """問い合わせメール一覧画面"""
    return render_template("list_contact_emails.html")


@app.route("/job-emails")
def list_job_emails() -> str:
    """求人関係メール一覧画面"""
    return render_template("list_job_emails.html")


@app.errorhandler(NotFound)
def show_404_page(error):
    msg = error.description
    logger.error("404エラー: %s", msg)
    return render_template("errors/404.html"), 404


@app.errorhandler(InternalServerError)
def show_500_page(error):
    msg = error.description
    logger.error("500エラー: %s", msg)
    return render_template("errors/500.html"), 500
