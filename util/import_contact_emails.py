"""問い合わせメールをCSVファイルからデータベースにインポートするスクリプト
使い方：python -m util.import_contact_emails /path/to/your/csvfile.csv
"""

import argparse
import csv
import os
import sys
from datetime import datetime

from app import create_app, db
from app.models import ContactEmail
from util.constants import CONTACT_TYPE_MAPPING, GENDER_MAPPING


def generate_contact_emails(csv_file_path: str):
    """
    CSVファイルから ContactEmail インスタンスを逐次生成するジェネレーター関数

    CSVファイルの各行は以下のカラム順とします:
        0: 問い合わせ種別 （例："その他"）
        1: 問い合わせ内容 (content)
        2: 名前
        3: ふりがな (kana)
        4: メールアドレス
        5: 性別（例："男性"）
        6: IP アドレス
        7: 受信日時 (例："2025.05.21 09:18:16")
    受信日時は "YYYY.MM.DD HH:MM:SS" の形式である必要があります。
    """
    if not os.path.exists(csv_file_path):
        raise FileNotFoundError(f"指定されたCSVファイルが存在しません: {csv_file_path}")

    with open(csv_file_path, "r", encoding="utf-8") as csvfile:
        # CSVのフィールド区切りはカンマ。値がダブルクォーテーションで囲まれている場合も自動で処理します。
        reader = csv.reader(csvfile, delimiter=",", quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            # 空行はスキップ
            if not row:
                continue

            # 必要なカラム数（8つ）が揃っていない場合はその行をスキップ
            if len(row) < 8:
                print(f"不正な形式の行をスキップ: {row}")
                continue

            (
                contact_type_str,
                content,
                name,
                kana,
                email,
                gender_str,
                ip,
                received_at_str,
            ) = row[:8]

            # 問い合わせ種別の変換
            contact_type = CONTACT_TYPE_MAPPING.get(contact_type_str.strip())
            if contact_type is None:
                print(f"不明な問い合わせ種別をスキップ: {contact_type_str}")
                continue

            # 性別の変換
            gender_value = gender_str.strip()
            if gender_value == "":
                gender = None
            else:
                gender = GENDER_MAPPING.get(gender_value)
                if gender is None:
                    print(f"不明な性別をスキップ: {gender_str}")
                    continue

            # 受信日時のパース（例："2025.05.21 09:18:16"）
            try:
                received_at = datetime.strptime(received_at_str.strip(), "%Y.%m.%d %H:%M:%S")
            except ValueError as e:
                print(f"日付フォーマットのエラー (行: {row}): {e}")
                continue

            yield ContactEmail(
                contact_type=contact_type,
                content=content.strip(),
                name=name.strip(),
                kana=kana.strip(),
                email=email.strip(),
                gender=gender,
                ip=ip.strip(),
                received_at=received_at,
            )


def import_csv(csv_file_path: str) -> None:
    """CSVファイルから ContactEmail データをデータベースにインポートする関数"""
    count = 0
    for contact_email in generate_contact_emails(csv_file_path):
        db.session.add(contact_email)
        count += 1

    try:
        db.session.commit()
        print(f"{count} 件の問い合わせメールをインポートしました。")
    except Exception as e:
        db.session.rollback()
        print(f"データベースへのコミット中にエラーが発生しました: {e}")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="CSVファイルから contact_emails テーブルへデータをインポートするスクリプト",
    )
    parser.add_argument("csv_file", help="インポートするCSVファイルのパス")
    args = parser.parse_args()

    # Flask アプリケーションの作成とアプリケーションコンテキストの開始
    app = create_app()
    with app.app_context():
        import_csv(args.csv_file)
