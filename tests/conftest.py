from datetime import datetime

import pytest

from app import create_app
from app.models import ContactEmail, JobEmail, db


@pytest.fixture
def app():
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Flaskのテストクライアント"""
    return app.test_client()


@pytest.fixture
def init_contact_emails(app):
    with app.app_context():
        db.session.add_all(
            [
                ContactEmail(
                    contact_type=1,
                    content="Test Content1",
                    name="山田太郎",
                    kana="ヤマダタロウ",
                    email="testemail1@example.com",
                    gender=1,
                    ip="192.168.1.1",
                    received_at=datetime(2024, 1, 1, 12, 0, 1),
                ),
                ContactEmail(
                    contact_type=1,
                    content="Test Content2",
                    name="鈴木次郎",
                    kana="スズキジロウ",
                    email="testemail2@example.com",
                    gender=2,
                    ip="192.168.1.2",
                    received_at=datetime(2024, 1, 2, 12, 0, 2),
                ),
            ]
        )
        db.session.commit()


@pytest.fixture
def init_job_emails(app):
    with app.app_context():
        db.session.add_all(
            [
                JobEmail(
                    subject="Test Subject1",
                    email="testemail1@example.com",
                    content="Test Content1",
                    received_at=datetime(2024, 1, 1, 12, 0, 1),
                ),
                JobEmail(
                    subject="Test Subject2",
                    email="testemai21@example.com",
                    content="Test Content2",
                    received_at=datetime(2024, 1, 2, 12, 0, 2),
                ),
            ]
        )
        db.session.commit()
