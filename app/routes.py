import logging

from flask import current_app as app
from flask import render_template
from werkzeug.exceptions import HTTPException, InternalServerError, NotFound

from app.models import ContactEmail, JobEmail

logger: logging.Logger = logging.getLogger(__name__)


@app.route("/")
def index() -> str:
    """トップ画面"""
    return render_template("index.html")


@app.route("/contact-emails")
def list_contact_emails() -> str:
    """問い合わせメール一覧画面"""
    mails = ContactEmail.query.order_by(ContactEmail.received_at.desc()).all()  # type: ignore
    return render_template("list_contact_emails.html", mails=mails)


@app.route("/job-emails")
def list_job_emails() -> str:
    """求人関係メール一覧画面"""
    mails = JobEmail.query.order_by(JobEmail.received_at.desc()).all()  # type: ignore
    return render_template("list_job_emails.html", mails=mails)


@app.errorhandler(NotFound)
def show_404_page(error: HTTPException) -> tuple[str, int]:
    """404 NotFoundエラー画面"""
    msg: str | None = error.description
    logger.error("404エラー: %s", msg)
    return render_template("errors/404.html"), 404


@app.errorhandler(InternalServerError)
def show_500_page(error: HTTPException) -> tuple[str, int]:
    """500 内部サーバーエラー画面"""
    msg: str | None = error.description
    logger.error("500エラー: %s", msg)
    return render_template("errors/500.html"), 500
