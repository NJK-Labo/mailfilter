"""
sample_module.py

このモジュールはサンプルデータを挿入するスクリプトを提供します。
各テーブルに25件のサンプルデータを挿入します。
開発環境の手動での動作確認で、もし必要があれば使用してください。

主な機能:
- データベースの既存データの削除
- ランダムなサンプルデータの生成と挿入

使用例:
    $ python insert_testdata.py

"""

import random
from datetime import datetime, timedelta

from app import create_app, db
from app.models import ContactEmail, JobEmail

app = create_app("development")


def insert_sample_data():
    """サンプルデータを挿入する関数"""
    with app.app_context():
        # テーブルをクリア
        db.session.query(ContactEmail).delete()
        db.session.query(JobEmail).delete()
        db.session.commit()
        print("既存のデータを削除しました。")

        sample_records = []

        # 過去30日間のランダムな日時を生成（25件分）
        random_dates = [
            datetime.now() - timedelta(days=random.randint(0, 30), minutes=random.randint(0, 1440)) for _ in range(25)
        ]

        # 日時を昇順にソート
        random_dates.sort()

        # 問い合わせメールデータを作成
        for i, received_at in enumerate(random_dates, start=1):
            sample_records.append(
                ContactEmail(
                    contact_type=random.randint(1, 5),  # ランダムな問い合わせ種別 (1〜5)
                    content=f"これはサンプルデータの問い合わせ内容 {i} 番目です。" * 10,
                    name=f"テストユーザー{i}",
                    kana=f"テスト ユーザー{i}",
                    email=f"user{i}@example.com",
                    gender=random.choice([1, 2]),  # ランダムな性別 (1=男性, 2=女性)
                    ip=f"192.168.1.{i}",  # IPアドレスをユニークにする
                    received_at=received_at,
                )
            )

        # 求人関連メールデータを作成
        for i, received_at in enumerate(random_dates, start=1):
            sample_records.append(
                JobEmail(
                    subject=f"サンプルデータの件名 {i} 番目",
                    email=f"user{i}@example.com",
                    content=f"これはサンプルデータの求人内容 {i} 番目です。" * 10,
                    received_at=received_at,
                )
            )

        db.session.add_all(sample_records)

        db.session.commit()
        print("各テーブルに25件のサンプルデータを挿入しました。")


if __name__ == "__main__":
    insert_sample_data()
