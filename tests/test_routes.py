from werkzeug.exceptions import InternalServerError


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
    assert b"Content1" in response.data
    assert b"Content2" in response.data

    # データが正しくソートされていることを確認（`received_at`の降順）
    assert response.data.index(b"Content2") < response.data.index(b"Content1")


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
