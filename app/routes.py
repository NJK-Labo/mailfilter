import logging

from flask import Blueprint, redirect, render_template, request, url_for
from werkzeug.exceptions import HTTPException, InternalServerError, NotFound

from app.models import ContactEmail, JobEmail

bp = Blueprint("main", __name__)

from app import db  # noqa: E402
from app.forms import ContactEmailSearchForm, JobEmailSearchForm  # noqa: E402
from app.services import search_contact_emails, search_job_emails, validate_input  # noqa: E402

logger: logging.Logger = logging.getLogger(__name__)


@bp.route("/")
def index() -> str:
    """トップ画面"""
    return render_template("index.html")


@bp.route("/contact-emails", methods=["GET"])
def list_contact_emails() -> str:
    """問い合わせメール一覧画面"""
    form = ContactEmailSearchForm(request.args)

    # 検索フォームの不正な入力値をクリア
    is_valid, cleaned_params = validate_input(form)

    if not is_valid:
        # 不正な値のクエリパラメータをクリアするためのリダイレクト
        return redirect(url_for("main.list_contact_emails", **cleaned_params))  # type: ignore

    mails = search_contact_emails(form)
    return render_template("list_contact_emails.html", mails=mails, form=form)


@bp.route("/contact-emails/<int:id>", methods=["GET"])
def show_contact_email(id):
    """問い合わせメール詳細画面"""
    mail = db.session.get(ContactEmail, id)
    return render_template("show_contact_email.html", mail=mail)


@bp.route("/job-emails")
def list_job_emails() -> str:
    """求人関係メール一覧画面"""
    form = JobEmailSearchForm(request.args)

    # 検索フォームの日付の不正な入力値をクリア
    is_valid, cleaned_params = validate_input(form)

    if not is_valid:
        # 不正な値のクエリパラメータをクリアするためのリダイレクト
        return redirect(url_for("main.list_job_emails", **cleaned_params))  # type: ignore

    mails = search_job_emails(form)
    return render_template("list_job_emails.html", mails=mails, form=form)


@bp.route("/job-emails/<int:id>", methods=["GET"])
def show_job_email(id):
    """求人関係メール詳細画面"""
    mail = db.session.get(JobEmail, id)
    return render_template("show_job_email.html", mail=mail)


@bp.app_errorhandler(NotFound)
def show_404_page(error: HTTPException) -> tuple[str, int]:
    """404 NotFoundエラー画面"""
    msg: str | None = error.description
    logger.error("404エラー: %s", msg)
    return render_template("errors/404.html"), 404


@bp.app_errorhandler(InternalServerError)
def show_500_page(error: HTTPException) -> tuple[str, int]:
    """500 内部サーバーエラー画面"""
    msg: str | None = error.description
    logger.error("500エラー: %s", msg)
    return render_template("errors/500.html"), 500
