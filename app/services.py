from datetime import datetime
from typing import Type

from flask_paginate import Pagination  # type: ignore
from flask_wtf import FlaskForm  # type: ignore
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import Query

from app.models import ContactEmail, JobEmail


def _replace_none_with_empty_string(params: dict[str, str]) -> dict[str, str]:
    """パラメータ内のNoneの値を空文字に修正する"""
    for key, value in params.items():
        if value is None:
            params[key] = ""
    return params


def validate_input(form: FlaskForm) -> tuple[bool, dict[str, str]]:
    """フォームのバリデーションを実行し、不正な値をクリアしたパラメータを返す"""
    is_valid = form.validate()
    if is_valid:
        return is_valid, form.data

    cleaned_params = form.data.copy()
    fields_to_check = list(form._fields.keys())
    for field in fields_to_check:
        if getattr(form, field).errors:
            cleaned_params[field] = ""

    cleaned_params = _replace_none_with_empty_string(cleaned_params)

    return is_valid, cleaned_params


def search_contact_emails(query: Query, form: FlaskForm) -> Query:
    """問い合わせメールの検索ロジック"""
    if form.start_date.data:
        query = query.filter(ContactEmail.received_at >= start_of_day(form.start_date.data))  # type: ignore
    if form.end_date.data:
        query = query.filter(ContactEmail.received_at <= end_of_day(form.end_date.data))  # type: ignore
    if form.keyword.data:
        # ユーザー入力のキーワードに含まれる特殊文字(%, _)をエスケープする
        keyword = f"%{form.keyword.data.replace('%', '\\%').replace('_', '\\_')}%"
        query = query.filter(
            ContactEmail.content.like(keyword, escape="\\")  # type: ignore
            | ContactEmail.name.like(keyword, escape="\\")  # type: ignore
            | ContactEmail.kana.like(keyword, escape="\\")  # type: ignore
            | ContactEmail.email.like(keyword, escape="\\")  # type: ignore
        )
    if form.type.data:
        query = query.filter(ContactEmail.contact_type == int(form.type.data))  # type: ignore

    return query


def search_job_emails(query: Query, form: FlaskForm) -> Query:
    """求人関係メールの検索ロジック"""
    if form.start_date.data:
        query = query.filter(JobEmail.received_at >= start_of_day(form.start_date.data))  # type: ignore
    if form.end_date.data:
        query = query.filter(JobEmail.received_at <= end_of_day(form.end_date.data))  # type: ignore
    if form.keyword.data:
        # ユーザー入力のキーワードに含まれる特殊文字(%, _)をエスケープする
        keyword = f"%{form.keyword.data.replace('%', '\\%').replace('_', '\\_')}%"
        query = query.filter(
            JobEmail.content.like(keyword, escape="\\")  # type: ignore
            | JobEmail.subject.like(keyword, escape="\\")  # type: ignore
            | JobEmail.email.like(keyword, escape="\\")  # type: ignore
        )

    return query


def start_of_day(date: datetime) -> datetime:
    """開始日の00:00:00を返す"""
    return datetime.combine(date, datetime.min.time())


def end_of_day(date: datetime) -> datetime:
    """終了日の23:59:59を返す"""
    return datetime.combine(date, datetime.max.time())


def paginate_query(query: Query, page: int, per_page: int) -> tuple[Query, Pagination]:
    """ページ送りのためのクエリを処理する関数"""
    mails = query.paginate(page=page, per_page=per_page, error_out=False)  # type: ignore
    pagination = Pagination(
        page=page,
        total=mails.total,
        record_name="mails",
        per_page=per_page,
        display_msg="{start} - {end} / {total} 件",
        css_framework="bootstrap5",
    )
    return mails, pagination


def sort_emails_by_received_at(query: Query, model: Type[DeclarativeMeta], order: str) -> Query:
    """メールのクエリ結果を受信日時で並び替える汎用関数"""
    if order == "asc":
        query = query.order_by(model.received_at.asc())  # type: ignore
    else:
        query = query.order_by(model.received_at.desc())  # type: ignore
    return query
