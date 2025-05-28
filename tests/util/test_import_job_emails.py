import os
import pytest
from datetime import datetime

from app.models import JobEmail
from util.import_job_emails import generate_job_emails, import_csv


def test_generate_job_emails_valid(tmp_path):
    """正常なCSV行からJobEmailインスタンスが生成されること"""
    csv_content = (
        "Subject 1,email1@example.com,Content 1,2025-05-26 15:44:10\n"
        "Subject 2,email2@example.com,Content 2,2025-05-26 15:44:20\n"
    )
    csv_file = tmp_path / "test_valid.csv"
    csv_file.write_text(csv_content, encoding="utf-8")

    emails = list(generate_job_emails(str(csv_file)))
    assert len(emails) == 2

    first = emails[0]
    assert first.subject == "Subject 1"
    assert first.email == "email1@example.com"
    assert first.content == "Content 1"
    assert first.received_at == datetime(2025, 5, 26, 15, 44, 10)


def test_generate_job_emails_invalid(tmp_path, capsys):
    """不正なCSV行（カラム数不足、日付フォーマットエラー）がスキップされること"""
    csv_content = (
        "Subject 1,email1@example.com,Content 1,2025-05-26 15:44:10\n"  # 正常行
        "Invalid Row Without Enough Columns\n"                         # カラム不足
        "Subject Wrong,email@example.com,Content Wrong,Not a date\n"      # 日付フォーマットエラー
        "Subject 2,email2@example.com,Content 2,2025-05-26 15:44:20\n"     # 正常行
    )
    csv_file = tmp_path / "test_invalid.csv"
    csv_file.write_text(csv_content, encoding="utf-8")

    emails = list(generate_job_emails(str(csv_file)))
    # 正常な行は2件のみ
    assert len(emails) == 2

    # エラーメッセージが標準出力に出力されていることを確認
    captured = capsys.readouterr().out
    assert "不正な形式の行をスキップ" in captured or "日付フォーマットのエラー" in captured


def test_generate_job_emails_file_not_found(tmp_path):
    """存在しないCSVファイルパスを指定した場合に FileNotFoundError が発生すること"""
    non_existent = tmp_path / "nonexistent.csv"
    with pytest.raises(FileNotFoundError):
        list(generate_job_emails(str(non_existent)))


def test_import_csv(app, db_session, tmp_path, capsys):
    """CSVファイルからDBへ正しくデータがコミットされること"""
    csv_content = (
        "Subject A,emailA@example.com,Content A,2025-05-26 15:44:10\n"
        "Subject B,emailB@example.com,Content B,2025-05-26 15:44:20\n"
    )
    csv_file = tmp_path / "test_import.csv"
    csv_file.write_text(csv_content, encoding="utf-8")

    # CSVからデータインポートを実行
    import_csv(str(csv_file))

    # インポート結果（標準出力）を検証
    captured = capsys.readouterr().out
    assert "2 件の求人関連メールをインポートしました" in captured

    # DBからインポートされたデータをクエリし、内容を検証
    emails = JobEmail.query.all()
    assert len(emails) == 2
    first = emails[0]
    assert first.subject == "Subject A"
    assert first.email == "emailA@example.com"