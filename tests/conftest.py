import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from datetime import datetime, timedelta

import pytest

from app import create_app
from app.models import ContactEmail, JobEmail, db


@pytest.fixture
def app():
    app = create_app("testing")
    app.config["WTF_CSRF_ENABLED"] = False  # CSRF 保護を無効化
    app.config["SERVER_NAME"] = "testserver"
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
def client(app, db_session):
    """Flaskのテストクライアント（dbセッションも初期化済み）"""
    return app.test_client()


@pytest.fixture
def init_contact_email(db_session):
    contact_email = ContactEmail(
        contact_type=1,
        content="Test Kensa01",
        name="検査一郎",
        kana="ケンサイチロウ",
        email="kensa1@example.com",
        gender=1,
        ip="10.0.0.10",
        received_at=datetime(2025, 1, 11, 10, 10, 11),
    )
    db_session.add(contact_email)
    db_session.commit()
    return contact_email


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
def init_job_email(db_session):
    job_email = JobEmail(
        subject="Test Kensa02",
        email="kensa02@example.com",
        content="検査02",
        received_at=datetime(2025, 1, 11, 12, 10, 12),
    )
    db_session.add(job_email)
    db_session.commit()
    return job_email


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
def init_contact_emails_for_specialchars_search(db_session):
    db_session.add_all(
        [
            ContactEmail(
                content="Test content 100%",
                name="Test name 1",
                kana="テストイチ",
                email="test1@example.com",
                contact_type=1,
                received_at=datetime(2025, 1, 9, 12, 0, 1),
                gender=1,
                ip="192.168.1.1",
            ),
            ContactEmail(
                content="Test content2 (・_・;)",
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
def init_job_emails_for_specialchars_search(db_session):
    db_session.add_all(
        [
            JobEmail(
                subject="Test subject 1 (・_・)",
                email="test1@example.com",
                content="Test content 1",
                received_at=datetime(2025, 1, 9, 12, 0, 1),
            ),
            JobEmail(
                subject="Test subject 2%",
                email="test2@example.com",
                content="Test content 2",
                received_at=datetime(2025, 2, 9, 12, 0, 2),
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


@pytest.fixture
def init_sort_emails(db_session):
    now = datetime.now()
    db_session.add_all(
        [
            ContactEmail(
                content="a",
                name="あ",
                kana="ア",
                email="test1@example.com",
                contact_type=1,
                received_at=now - timedelta(days=3),
                gender=1,
                ip="172.16.1.1",
            ),
            ContactEmail(
                content="b",
                name="い",
                kana="イ",
                email="test2@example.com",
                contact_type=2,
                received_at=now - timedelta(days=2),
                gender=2,
                ip="172.16.1.2",
            ),
            ContactEmail(
                content="c",
                name="う",
                kana="ウ",
                email="test3@example.com",
                contact_type=3,
                received_at=now - timedelta(days=1),
                gender=1,
                ip="172.16.1.3",
            ),
        ]
    )
    db_session.commit()
