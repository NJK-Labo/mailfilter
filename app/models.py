from datetime import datetime

from app import db
from config import Config


class ContactEmail(db.Model):  # type: ignore
    """問い合わせメール"""

    __tablename__: str = "contact_emails"

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 問い合わせ種別
    # （1: 採用情報について, 2: 取り扱い製品について, 3: 事業内容について, 4: プライバシーポリシーについて, 5: その他）
    contact_type: int = db.Column(db.Integer, nullable=False)
    content: str = db.Column(db.Text(3000), nullable=False)
    name: str = db.Column(db.String(200), nullable=False)
    kana: str = db.Column(db.String(200), nullable=False)
    email: str = db.Column(db.String(200), nullable=False)
    # 性別（1: 男性, 2: 女性）
    gender: int = db.Column(db.Integer, nullable=False)
    ip: str = db.Column(db.String(200), nullable=False)
    received_at: datetime = db.Column(db.DateTime, nullable=False, index=True, default=Config.now_jst)
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=Config.now_jst)
    updated_at: datetime = db.Column(db.DateTime, nullable=True, default=Config.now_jst, onupdate=Config.now_jst)


class JobEmail(db.Model):  # type: ignore
    """求人関連メール"""

    __tablename__: str = "job_emails"

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject: str = db.Column(db.String(200), nullable=False)
    email: str = db.Column(db.String(200), nullable=False)
    content: str = db.Column(db.Text, nullable=False)
    received_at: datetime = db.Column(db.DateTime, nullable=False, index=True, default=Config.now_jst)
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=Config.now_jst)
    updated_at: datetime = db.Column(db.DateTime, nullable=True, default=Config.now_jst, onupdate=Config.now_jst)
