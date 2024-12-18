import pytest

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
