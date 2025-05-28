"""求人関連メールをCSVファイルからデータベースにインポートするスクリプト
使い方：python -m util.import_job_emails /path/to/your/csvfile.csv
"""

import csv
import os
import sys
from datetime import datetime
import argparse

from app import create_app, db
from app.models import JobEmail


def generate_job_emails(csv_file_path: str):
    """CSVファイルから JobEmail インスタンスを逐次生成するジェネレーター関数

    CSVファイルの各行は以下のカラム順とします:
        subject, email, content, received_at
    受信日時は "YYYY-MM-DD HH:MM:SS" の形式である必要があります。
    """
    if not os.path.exists(csv_file_path):
        raise FileNotFoundError(f"指定されたCSVファイルが存在しません: {csv_file_path}")

    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        # CSVのフィールド区切りはカンマです。値がダブルクォーテーションで囲まれている場合も、囲まれていない場合も自動的に処理します。
        reader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        
        for row in reader:
            # 空行はスキップ
            if not row:
                continue

            # 必要なカラム数（4つ）が揃っていない場合は、その行をスキップ
            if len(row) < 4:
                print(f"不正な形式の行をスキップ: {row}")
                continue

            subject, email, content, received_at_str = row[:4]

            # 受信日時のパース（例: "2025-05-28 13:12:35" の形式）
            try:
                received_at = datetime.strptime(received_at_str.strip(), "%Y-%m-%d %H:%M:%S")
            except ValueError as e:
                print(f"日付フォーマットのエラー (行: {row}): {e}")
                continue

            yield JobEmail(
                subject=subject.strip(),
                email=email.strip(),
                content=content.strip(),
                received_at=received_at
            )


def import_csv(csv_file_path: str) -> None:
    """CSVファイルから JobEmail データをデータベースにインポートする関数"""
    count = 0
    for job_email in generate_job_emails(csv_file_path):
        db.session.add(job_email)
        count += 1

    try:
        db.session.commit()
        print(f"{count} 件の求人関連メールをインポートしました。")
    except Exception as e:
        db.session.rollback()
        print(f"データベースへのコミット中にエラーが発生しました: {e}")
        sys.exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="CSVファイルから job_emails テーブルへデータをインポートするスクリプト"
    )
    parser.add_argument("csv_file", help="インポートするCSVファイルのパス")
    args = parser.parse_args()

    # Flask アプリケーションの作成とアプリケーションコンテキストの開始
    app = create_app()
    with app.app_context():
        import_csv(args.csv_file)
