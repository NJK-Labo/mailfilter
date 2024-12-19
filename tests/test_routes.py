import pytest
from werkzeug.exceptions import InternalServerError

from app import create_app


@pytest.fixture
def client():
    app = create_app("testing")
    app.testing = True
    with app.test_client() as client:
        with app.app_context():
            yield client


def test_index(client):
    """トップ画面のテスト"""
    response = client.get("/")
    assert response.status_code == 200
    assert "一覧画面を表示".encode("utf-8") in response.data


def test_404_error(client):
    """404エラーのハンドラテスト"""
    response = client.get("/non-existent-page")
    assert response.status_code == 404
    assert b"404 Not Found" in response.data


def test_500_error(client):
    """500エラーのハンドラテスト"""

    @client.application.route("/cause-error")
    def cause_error():
        raise InternalServerError("故意の500エラー")

    response = client.get("/cause-error")
    assert response.status_code == 500
    assert b"Internal Server Error" in response.data
