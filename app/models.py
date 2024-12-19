from datetime import datetime

from app import db
from config import Config


class ContactEmail(db.Model):  # type: ignore
    __tablename__: str = "contact_emails"

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    contact_type: int = db.Column(db.Integer, nullable=False)
    content: str = db.Column(db.Text, nullable=False)
    name: str = db.Column(db.String(200), nullable=False)
    kana: str = db.Column(db.String(200), nullable=False)
    email: str = db.Column(db.String(200), nullable=False)
    gender: int = db.Column(db.Integer, nullable=False)
    ip: str = db.Column(db.String(200), nullable=False)
    received_at: datetime = db.Column(db.DateTime, nullable=False, index=True, default=Config.now_jst)
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=Config.now_jst)
    updated_at: datetime = db.Column(db.DateTime, nullable=False, default=Config.now_jst, onupdate=Config.now_jst)


class JobEmail(db.Model):  # type: ignore
    __tablename__: str = "job_emails"

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject: str = db.Column(db.String(200), nullable=False)
    email: str = db.Column(db.String(200), nullable=False)
    content: str = db.Column(db.Text, nullable=False)
    received_at: datetime = db.Column(db.DateTime, nullable=False, index=True, default=Config.now_jst)
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=Config.now_jst)
    updated_at: datetime = db.Column(db.DateTime, nullable=False, default=Config.now_jst, onupdate=Config.now_jst)
