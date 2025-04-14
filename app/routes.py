import logging

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask.typing import ResponseReturnValue
from flask_paginate import get_page_parameter  # type: ignore
from werkzeug.exceptions import HTTPException, InternalServerError, NotFound

from app import db, services
from app.forms import AccessButtonForm, ContactEmailSearchForm, JobEmailSearchForm, MailDeleteButtonForm, NjkMemoForm
from app.models import ContactEmail, JobEmail

bp = Blueprint("main", __name__)
logger: logging.Logger = logging.getLogger(__name__)

# ページ送り機能の1ページ当たり表示件数
PER_PAGE: int = 10


@bp.route("/")
def index() -> ResponseReturnValue:
    """トップ画面"""
    return render_template("index.html")


@bp.route("/contact-emails", methods=["GET", "DELETE"])
def list_contact_emails() -> ResponseReturnValue:
    """問い合わせメール一覧画面"""
    form = ContactEmailSearchForm(request.args)

    # 検索フォームの不正な入力値をクリア
    is_valid, cleaned_params = services.validate_input(form)

    if not is_valid:
        # 不正な値のクエリパラメータをクリアするためのリダイレクト
        return redirect(url_for("main.list_contact_emails", **cleaned_params))  # type: ignore

    # フォームの検索結果
    query = ContactEmail.query
    query = services.search_contact_emails(query=query, form=form)

    # 並べ替え機能
    order = request.args.get("order", "desc")
    query = services.sort_emails_by_received_at(query=query, model=ContactEmail, order=order)

    # ページ送り機能
    page = request.args.get(get_page_parameter(), type=int, default=1)
    mails, pagination = services.paginate_query(query=query, page=page, per_page=PER_PAGE)

    delete_button_form = MailDeleteButtonForm()
    access_button_form = AccessButtonForm()

    return render_template(
        "list_contact_emails.html",
        mails=mails,
        form=form,
        pagination=pagination,
        delete_button_form=delete_button_form,
        access_button_form=access_button_form,
        )


@bp.route("/contact-emails/<int:id>", methods=["GET"])
def show_contact_email(id: int) -> ResponseReturnValue:
    """問い合わせメール詳細画面"""
    mail = db.session.get(ContactEmail, id)
    if not mail:
        abort(404)
    form = NjkMemoForm(njk_memo=mail.njk_memo)
    return render_template("show_contact_email.html", mail=mail, form=form)


@bp.route("/contact-emails/<int:id>/update", methods=["POST"])
def update_contact_email(id: int) -> ResponseReturnValue:
    """問い合わせメールの更新処理"""
    mail = db.session.get(ContactEmail, id)
    if not mail:
        abort(404)

    form = NjkMemoForm()
    if form.validate_on_submit():
        mail.njk_memo = form.njk_memo.data
        # 入力が空文字や空白のみの場合は False、それ以外は True
        mail.is_njk_memo_present = bool(form.njk_memo.data.strip())
        db.session.commit()
        flash("NJK記入欄を保存しました", "success")
    else:
        flash("入力内容にエラーがあります。再度ご確認ください。", "warning")

    return redirect(url_for("main.show_contact_email", id=id))


@bp.route("/contact_emails/<int:id>", methods=["POST"])
def delete_contact_email(id: int) -> ResponseReturnValue:
    """問い合わせメール削除"""
    mail = db.session.get(ContactEmail, id)
    if not mail:
        abort(404)
    db.session.delete(mail)
    db.session.commit()
    flash("問い合わせメールが削除されました", "success")

    # 検索条件を削除前の状態に設定する
    search_params = request.form.to_dict()
    search_params.pop('csrf_token', None)  # csrf_tokenは不要
    return redirect(url_for("main.list_contact_emails", **search_params))  # type: ignore


@bp.route("/job-emails", methods=["GET", "DELETE"])
def list_job_emails() -> ResponseReturnValue:
    """求人関係メール一覧画面"""
    form = JobEmailSearchForm(request.args)

    # 検索フォームの日付の不正な入力値をクリア
    is_valid, cleaned_params = services.validate_input(form)

    if not is_valid:
        # 不正な値のクエリパラメータをクリアするためのリダイレクト
        return redirect(url_for("main.list_job_emails", **cleaned_params))  # type: ignore

    # フォームの検索結果
    query = JobEmail.query
    query = services.search_job_emails(query=query, form=form)

    # 並べ替え機能
    order = request.args.get("order", "desc")
    query = services.sort_emails_by_received_at(query=query, model=JobEmail, order=order)

    # ページ送り機能
    page = request.args.get(get_page_parameter(), type=int, default=1)
    mails, pagination = services.paginate_query(query=query, page=page, per_page=PER_PAGE)

    delete_button_form = MailDeleteButtonForm()
    access_button_form = AccessButtonForm()

    return render_template(
        "list_job_emails.html",
        mails=mails,
        form=form,
        pagination=pagination,
        delete_button_form=delete_button_form,
        access_button_form=access_button_form,
        )


@bp.route("/job-emails/<int:id>", methods=["GET"])
def show_job_email(id: int) -> ResponseReturnValue:
    """求人関係メール詳細画面"""
    mail = db.session.get(JobEmail, id)
    if not mail:
        abort(404)
    form = NjkMemoForm(njk_memo=mail.njk_memo)
    return render_template("show_job_email.html", mail=mail, form=form)


@bp.route("/job-emails/<int:id>/update", methods=["POST"])
def update_job_email(id: int) -> ResponseReturnValue:
    """求人関係メールの更新処理"""
    mail = db.session.get(JobEmail, id)
    if not mail:
        abort(404)

    form = NjkMemoForm()
    if form.validate_on_submit():
        mail.njk_memo = form.njk_memo.data
        # 入力が空文字や空白のみの場合は False、それ以外は True
        mail.is_njk_memo_present = bool(form.njk_memo.data.strip())
        db.session.commit()
        flash("NJK記入欄を保存しました", "success")
    else:
        flash("入力内容にエラーがあります。再度ご確認ください。", "warning")

    return redirect(url_for("main.show_job_email", id=id))


@bp.route("/job_emails/<int:id>", methods=["POST"])
def delete_job_email(id: int) -> ResponseReturnValue:
    """求人関係メール削除"""
    mail = db.session.get(JobEmail, id)
    if not mail:
        abort(404)
    db.session.delete(mail)
    db.session.commit()
    flash("求人関係メールが削除されました", "success")

    # 検索条件を削除前の状態に設定する
    search_params = request.form.to_dict()
    search_params.pop('csrf_token', None)  # csrf_tokenは不要
    return redirect(url_for("main.list_job_emails", **search_params))  # type: ignore


@bp.route("/contact-emails/<int:id>/access", methods=["POST"])
def access_contact_email(id: int) -> ResponseReturnValue:
    """問い合わせメールアクセス処理"""
    mail = db.session.get(ContactEmail, id)
    if not mail:
        abort(404)
    mail.is_detail_accessed = True
    db.session.commit()

    return redirect(url_for("main.show_contact_email", id=id))


@bp.route("/job-emails/<int:id>/access", methods=["POST"])
def access_job_email(id: int) -> ResponseReturnValue:
    """求人関係メールアクセス処理"""
    mail = db.session.get(JobEmail, id)
    if not mail:
        abort(404)
    mail.is_detail_accessed = True
    db.session.commit()

    return redirect(url_for("main.show_job_email", id=id))


@bp.app_errorhandler(NotFound)
def show_404_page(error: HTTPException) -> ResponseReturnValue:
    """404 NotFoundエラー画面"""
    msg: str | None = error.description
    logger.error("404エラー: %s", msg)
    return render_template("errors/404.html"), 404


@bp.app_errorhandler(InternalServerError)
def show_500_page(error: HTTPException) -> ResponseReturnValue:
    """500 内部サーバーエラー画面"""
    msg: str | None = error.description
    logger.error("500エラー: %s", msg, exc_info=True)
    return render_template("errors/500.html"), 500
