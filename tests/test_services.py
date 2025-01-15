from app.forms import ContactEmailSearchForm, JobEmailSearchForm
from app.models import ContactEmail, JobEmail
from app.services import _replace_none_with_empty_string, search_contact_emails, search_job_emails, validate_input
from tests.mock import MockSearchForm


def test_replace_none_with_empty_string():
    """パラメータ内のNoneの値を空文字に修正するテスト"""
    params = {"key1": "value1", "key2": None, "key3": ""}
    expected_result = {"key1": "value1", "key2": "", "key3": ""}
    assert _replace_none_with_empty_string(params) == expected_result


def test_validate_input_valid_form():
    """検索フォームのバリデーションが成功した場合は、入力値をそのまま返す"""
    form_data = {"field1": "value1", "field2": "value2"}
    form = MockSearchForm(data=form_data, is_valid=True, errors={})

    is_valid, cleaned_params = validate_input(form)

    assert is_valid is True
    assert cleaned_params == form_data


def test_validate_input_invalid_form():
    """検索フォームのバリデーションが失敗した場合は、不正な値をクリアしたパラメータを返す"""
    form_data = {"field1": "value1", "field2": "invalid", "field3": "value3"}
    form = MockSearchForm(data=form_data, is_valid=False, errors={"field2": ["error"]})
    form._fields["field2"].errors.append("error")

    is_valid, cleaned_params = validate_input(form)

    assert is_valid is False
    assert cleaned_params == {"field1": "value1", "field2": "", "field3": "value3"}


# 問い合わせメールの検索ロジックのテスト
def test_search_contact_emails_no_filters(client, init_contact_emails_for_search):
    """検索条件がない場合は全てのメールを返す"""
    form = ContactEmailSearchForm()
    form.start_date.data = ""
    form.end_date.data = ""
    form.keyword.data = ""
    form.type.data = ""

    query = ContactEmail.query
    query = search_contact_emails(query, form)
    results = query.all()
    assert len(results) == 2


def test_search_contact_emails_with_start_date(client, init_contact_emails_for_search):
    """開始日付のみ指定した場合は、その日付以降のメールを返す"""
    form = ContactEmailSearchForm()
    form.start_date.data = "2025-02-01"
    form.end_date.data = ""
    form.keyword.data = ""
    form.type.data = ""

    query = ContactEmail.query
    query = search_contact_emails(query, form)
    results = query.all()
    assert len(results) == 1
    assert results[0].content == "Test content 2"


def test_search_contact_emails_with_end_date(client, init_contact_emails_for_search):
    """終了日付のみ指定した場合は、その日付以前のメールを返す"""
    form = ContactEmailSearchForm()
    form.start_date.data = ""
    form.end_date.data = "2025-01-31"
    form.keyword.data = ""
    form.type.data = ""

    query = ContactEmail.query
    query = search_contact_emails(query, form)
    results = query.all()
    assert len(results) == 1
    assert results[0].content == "Test content 1"


def test_search_contact_emails_with_keyword(client, init_contact_emails_for_search):
    """キーワードのみ指定した場合は、そのキーワードを含むメールを返す"""
    form = ContactEmailSearchForm()
    form.start_date.data = ""
    form.end_date.data = ""
    form.keyword.data = "content 2"
    form.type.data = ""

    query = ContactEmail.query
    query = search_contact_emails(query, form)
    results = query.all()
    assert len(results) == 1
    assert results[0].content == "Test content 2"


def test_search_contact_emails_with_type(client, init_contact_emails_for_search):
    """問い合わせ種別のみ指定した場合は、その種別のメールを返す"""
    form = ContactEmailSearchForm()
    form.start_date.data = ""
    form.end_date.data = ""
    form.keyword.data = ""
    form.type.data = 1

    query = ContactEmail.query
    query = search_contact_emails(query, form)
    results = query.all()
    assert len(results) == 1
    assert results[0].content == "Test content 1"


def test_search_contact_emails_with_all_filters(client, init_contact_emails_for_search):
    """全ての条件を指定した場合は、全ての条件に合致するメールを返す"""
    form = ContactEmailSearchForm()
    form.start_date.data = "2025-01-01"
    form.end_date.data = "2025-02-01"
    form.keyword.data = "Test content 1"
    form.type.data = 1

    query = ContactEmail.query
    query = search_contact_emails(query, form)
    results = query.all()
    assert len(results) == 1
    assert results[0].content == "Test content 1"


# 求人関係メールの検索ロジックのテスト
def test_search_job_emails_no_filters(client, init_job_emails_for_search):
    """検索条件がない場合は全てのメールを返す"""
    form = JobEmailSearchForm()
    form.start_date.data = ""
    form.end_date.data = ""
    form.keyword.data = ""

    query = JobEmail.query
    query = search_job_emails(query, form)
    results = query.all()
    assert len(results) == 2


def test_search_job_emails_with_start_date(client, init_job_emails_for_search):
    """開始日付のみ指定した場合は、その日付以降のメールを返す"""
    form = JobEmailSearchForm()
    form.start_date.data = "2025-02-01"
    form.end_date.data = ""
    form.keyword.data = ""

    query = JobEmail.query
    query = search_job_emails(query, form)
    results = query.all()
    assert len(results) == 1
    assert results[0].content == "Test content 2"


def test_search_job_emails_with_end_date(client, init_job_emails_for_search):
    """終了日付のみ指定した場合は、その日付以前のメールを返す"""
    form = JobEmailSearchForm()
    form.start_date.data = ""
    form.end_date.data = "2025-01-31"
    form.keyword.data = ""

    query = JobEmail.query
    query = search_job_emails(query, form)
    results = query.all()
    assert len(results) == 1
    assert results[0].content == "Test content 1"


def test_search_job_emails_with_keyword(client, init_job_emails_for_search):
    """キーワードのみ指定した場合は、そのキーワードを含むメールを返す"""
    form = JobEmailSearchForm()
    form.start_date.data = ""
    form.end_date.data = ""
    form.keyword.data = "content 2"

    query = JobEmail.query
    query = search_job_emails(query, form)
    results = query.all()
    assert len(results) == 1
    assert results[0].content == "Test content 2"


def test_search_job_emails_with_all_filters(client, init_job_emails_for_search):
    """全ての条件を指定した場合は、全ての条件に合致するメールを返す"""
    form = JobEmailSearchForm()
    form.start_date.data = "2025-01-01"
    form.end_date.data = "2025-02-01"
    form.keyword.data = "Test content 1"

    query = JobEmail.query
    query = search_job_emails(query, form)
    results = query.all()
    assert len(results) == 1
    assert results[0].content == "Test content 1"
