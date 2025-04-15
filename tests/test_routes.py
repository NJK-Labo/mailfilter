from urllib.parse import urlparse

from flask import url_for
from werkzeug.exceptions import InternalServerError

from app.models import ContactEmail, JobEmail


def test_index(client):
    """トップ画面のテスト"""
    response = client.get("/")
    assert response.status_code == 200
    assert "一覧画面を表示します".encode("utf-8") in response.data


def test_list_contact_emails(client, init_contact_emails):
    """問い合わせメール一覧画面で複数件のレコードが正しく表示されるかテスト"""
    response = client.get("/contact-emails")
    assert response.status_code == 200
    assert b"Content1" in response.data
    assert b"Content2" in response.data

    # データが正しくソートされていることを確認（`received_at`の降順）
    assert response.data.index(b"Content2") < response.data.index(b"Content1")


def test_list_job_emails(client, init_job_emails):
    """求人関係メール一覧画面で複数件のレコードが正しく表示されるかテスト"""
    response = client.get("/job-emails")
    assert response.status_code == 200
    assert b"Subject1" in response.data
    assert b"Subject2" in response.data

    # データが正しくソートされていることを確認（`received_at`の降順）
    assert response.data.index(b"Subject2") < response.data.index(b"Subject1")


def test_show_contact_email(client, init_contact_emails):
    """問い合わせメール詳細画面のテスト"""
    response = client.get("/contact-emails/1")
    assert response.status_code == 200
    assert b"Content1" in response.data
    assert b"testemail1" in response.data


def test_show_contact_email_not_found(client, init_contact_emails):
    """問い合わせメールが見つからない場合の詳細画面のテスト"""
    response = client.get("/contact-emails/999999")
    assert response.status_code == 404
    assert "お探しのページは見つかりませんでした".encode("utf-8") in response.data


def test_delete_contact_email(client, init_contact_emails):
    """問い合わせメール削除のテスト"""
    response = client.post("/contact_emails/1", data={"_method": "DELETE"})
    assert response.status_code == 302
    url = url_for("main.list_contact_emails", _external=True)
    assert response.headers["Location"] == urlparse(url).path

    # リダイレクト先のページを取得
    redirect_response = client.get(response.headers["Location"], follow_redirects=True)
    assert "問い合わせメールが削除されました" in redirect_response.data.decode("utf-8")


def test_show_job_email(client, init_job_emails):
    """求人関係メール詳細画面のテスト"""
    response = client.get("/job-emails/1")
    assert response.status_code == 200
    assert b"Subject1" in response.data
    assert b"Content1" in response.data


def test_show_job_email_not_found(client, init_job_emails):
    """求人関係メールが見つからない場合の詳細画面のテスト"""
    response = client.get("/job-emails/999999")
    assert response.status_code == 404
    assert "お探しのページは見つかりませんでした".encode("utf-8") in response.data


def test_delete_job_email(client, init_job_emails):
    """求人関係メール削除のテスト"""
    response = client.post("/job_emails/1", data={"_method": "DELETE"})
    assert response.status_code == 302
    url = url_for("main.list_job_emails", _external=True)
    assert response.headers["Location"] == urlparse(url).path

    # リダイレクト先のページを取得
    redirect_response = client.get(response.headers["Location"], follow_redirects=True)
    assert "求人関係メールが削除されました" in redirect_response.data.decode("utf-8")


def test_404_error(client):
    """404エラーのハンドラテスト"""
    response = client.get("/non-existent-page")
    assert response.status_code == 404
    assert "お探しのページは見つかりませんでした".encode("utf-8") in response.data


def test_500_error(client):
    """500エラーのハンドラテスト"""

    @client.application.route("/cause-error")
    def cause_error():
        raise InternalServerError("故意の500エラー")

    response = client.get("/cause-error")
    assert response.status_code == 500
    assert "サーバーエラーが発生しました".encode("utf-8") in response.data


def test_update_contact_email_valid(client, db_session, init_contact_email):
    """
    問い合わせメール更新テスト（有効な入力: 100文字以内、通常テキスト）
    """
    mail_id = init_contact_email.id
    new_memo = "更新済みメモの内容"
    response = client.post(
        f"/contact-emails/{mail_id}/update",
        data={"njk_memo": new_memo},
        follow_redirects=True
    )
    # 正常なリダイレクトが完了していれば、200が返る
    assert response.status_code == 200

    updated_mail = db_session.get(ContactEmail, mail_id)
    # メモが更新され、空白でないため is_njk_memo_present が True となる
    assert updated_mail.njk_memo == new_memo
    assert updated_mail.is_njk_memo_present is True


def test_update_contact_email_valid_whitespace(client, db_session, init_contact_email):
    """
    問い合わせメール更新テスト（有効な入力: 空白のみ）

    ※空白のみの入力はエラーにならず、更新は成功するが、
      入力値をstrip()した結果は空文字となるため is_njk_memo_present は False となる。
    """
    mail_id = init_contact_email.id
    whitespace_input = "     "  # 空白のみ
    response = client.post(
        f"/contact-emails/{mail_id}/update",
        data={"njk_memo": whitespace_input},
        follow_redirects=True
    )
    assert response.status_code == 200

    updated_mail = db_session.get(ContactEmail, mail_id)
    assert updated_mail.njk_memo == whitespace_input
    assert updated_mail.is_njk_memo_present is False


def test_update_contact_email_over_length(client, db_session, init_contact_email):
    """
    問い合わせメール更新テスト（無効な入力: 100文字を超える）

    ※入力が101文字以上の場合、フォームバリデーションでエラーとなり、更新されないことを検証
      （Flashエラーメッセージ "入力内容にエラーがあります。再度ご確認ください。" が表示される
    """
    mail_id = init_contact_email.id
    original_memo = init_contact_email.njk_memo
    over_length_input = "a" * 101  # 101文字の入力
    response = client.post(
        f"/contact-emails/{mail_id}/update",
        data={"njk_memo": over_length_input},
        follow_redirects=True
    )
    assert response.status_code == 200

    updated_mail = db_session.get(ContactEmail, mail_id)
    # バリデーションエラー発生の場合、更新は行われず元の値が保持される
    assert updated_mail.njk_memo == original_memo
    # エラーFlashメッセージの確認
    assert "入力内容にエラーがあります".encode("utf-8") in response.data


def test_update_job_email_valid(client, db_session, init_job_email):
    """
    求人メール更新テスト（有効な入力: 100文字以内、通常テキスト）
    """
    mail_id = init_job_email.id
    new_memo = "求人メールの更新済みメモ"
    response = client.post(
        f"/job-emails/{mail_id}/update",
        data={"njk_memo": new_memo},
        follow_redirects=True
    )
    assert response.status_code == 200

    updated_mail = db_session.get(JobEmail, mail_id)
    assert updated_mail.njk_memo == new_memo
    assert updated_mail.is_njk_memo_present is True


def test_update_job_email_valid_whitespace(client, db_session, init_job_email):
    """
    求人メール更新テスト（有効な入力: 空白のみ）

    ※空白のみの入力は更新は成功するが、is_njk_memo_present は False になる。
    """
    mail_id = init_job_email.id
    whitespace_input = "      "
    response = client.post(
        f"/job-emails/{mail_id}/update",
        data={"njk_memo": whitespace_input},
        follow_redirects=True
    )
    assert response.status_code == 200

    updated_mail = db_session.get(JobEmail, mail_id)
    assert updated_mail.njk_memo == whitespace_input
    assert updated_mail.is_njk_memo_present is False


def test_update_job_email_over_length(client, db_session, init_job_email):
    """
    求人メール更新テスト（無効な入力: 100文字を超える）

    ※101文字以上の入力の場合、バリデーションエラーとなり、更新されないことを検証。
    """
    mail_id = init_job_email.id
    original_memo = init_job_email.njk_memo
    over_length_input = "b" * 101
    response = client.post(
        f"/job-emails/{mail_id}/update",
        data={"njk_memo": over_length_input},
        follow_redirects=True
    )
    assert response.status_code == 200

    updated_mail = db_session.get(JobEmail, mail_id)
    # 入力が更新されず、元の値がそのまま残ることを確認
    assert updated_mail.njk_memo == original_memo
    # エラーFlashメッセージの確認
    assert "入力内容にエラーがあります".encode("utf-8") in response.data


def test_update_contact_email_not_found(client):
    """
    存在しない問い合わせメールIDに対する更新では、404エラーとなる。
    """
    nonexistent_id = 9999  # 存在しないID
    response = client.post(
        f"/contact-emails/{nonexistent_id}/update",
        data={"njk_memo": "何かしらのメモ"},
        follow_redirects=True
    )
    assert response.status_code == 404


def test_update_job_email_not_found(client):
    """
    存在しない求人メールIDに対する更新では、404エラーとなる。
    """
    nonexistent_id = 9999  # 存在しないID
    response = client.post(
        f"/job-emails/{nonexistent_id}/update",
        data={"njk_memo": "何かしらのメモ"},
        follow_redirects=True
    )
    assert response.status_code == 404
