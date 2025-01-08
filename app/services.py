from typing import Dict, Tuple

from app.models import ContactEmail, JobEmail


def replace_none_with_empty_string(params: Dict[str, str]) -> Dict[str, str]:
    """パラメータ内のNoneの値を空文字に修正する"""
    for key, value in params.items():
        if value is None:
            params[key] = ""
    return params


def validate_input(form) -> Tuple[bool, Dict[str, str]]:
    """フォームのバリデーションを実行し、不正な値をクリアしたパラメータを返す"""
    is_valid = form.validate()
    if is_valid:
        return is_valid, form.data

    cleaned_params = form.data.copy()
    fields_to_check = list(form._fields.keys())
    for field in fields_to_check:
        if getattr(form, field).errors:
            cleaned_params[field] = ""

    cleaned_params = replace_none_with_empty_string(cleaned_params)

    return is_valid, cleaned_params


def search_contact_emails(form) -> list[ContactEmail]:
    """問い合わせメールの検索ロジック"""
    query = ContactEmail.query.order_by(ContactEmail.received_at.desc())  # type: ignore
    if form.start_date.data:
        query = query.filter(ContactEmail.received_at >= form.start_date.data)
    if form.end_date.data:
        query = query.filter(ContactEmail.received_at <= form.end_date.data)
    if form.keyword.data:
        query = query.filter(
            ContactEmail.content.like(f"%{form.keyword.data}%")  # type: ignore
            | ContactEmail.name.like(f"%{form.keyword.data}%")  # type: ignore
            | ContactEmail.kana.like(f"%{form.keyword.data}%")  # type: ignore
            | ContactEmail.email.like(f"%{form.keyword.data}%")  # type: ignore
        )
    if form.type.data:
        query = query.filter(ContactEmail.contact_type == int(form.type.data))

    return query.all()


def search_job_emails(form) -> list[JobEmail]:
    """問い合わせメールの検索ロジック"""
    query = JobEmail.query.order_by(JobEmail.received_at.desc())  # type: ignore
    if form.start_date.data:
        query = query.filter(JobEmail.received_at >= form.start_date.data)
    if form.end_date.data:
        query = query.filter(JobEmail.received_at <= form.end_date.data)
    if form.keyword.data:
        query = query.filter(
            JobEmail.content.like(f"%{form.keyword.data}%")  # type: ignore
            | JobEmail.subject.like(f"%{form.keyword.data}%")  # type: ignore
            | JobEmail.email.like(f"%{form.keyword.data}%")  # type: ignore
        )

    return query.all()
