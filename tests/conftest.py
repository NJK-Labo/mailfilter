import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from datetime import datetime

import pytest

from app import create_app
from app.models import ContactEmail, JobEmail, db


@pytest.fixture
def app():
    app = create_app("testing")
    with app.app_context():
        yield app


@pytest.fixture
def db_session(app):
    with app.app_context():
        db.create_all()
        yield db.session
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Flaskのテストクライアント"""
    return app.test_client()


@pytest.fixture
def init_contact_emails(db_session):
    db_session.add_all(
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
    db_session.commit()


@pytest.fixture
def init_job_emails(db_session):
    db_session.add_all(
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
    db_session.commit()


@pytest.fixture
def init_contact_emails_for_search(db_session):
    db_session.add_all(
        [
            ContactEmail(
                content="Test content 1",
                name="Test name 1",
                kana="テストイチ",
                email="test1@example.com",
                contact_type=1,
                received_at=datetime(2025, 1, 9, 12, 0, 1),
                gender=1,
                ip="192.168.1.1",
            ),
            ContactEmail(
                content="Test content 2",
                name="Test name 2",
                kana="テストニ",
                email="test2@example.com",
                contact_type=2,
                received_at=datetime(2025, 2, 9, 12, 0, 2),
                gender=2,
                ip="192.168.1.2",
            ),
        ]
    )
    db_session.commit()


@pytest.fixture
def init_job_emails_for_search(db_session):
    db_session.add_all(
        [
            JobEmail(
                subject="Test subject 1",
                email="test1@example.com",
                content="Test content 1",
                received_at=datetime(2025, 1, 9, 12, 0, 1),
            ),
            JobEmail(
                subject="Test subject 2",
                email="test2@example.com",
                content="Test content 2",
                received_at=datetime(2025, 2, 9, 12, 0, 2),
            ),
        ]
    )
    db_session.commit()
