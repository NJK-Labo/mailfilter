import pytest
from datetime import datetime
from app.models import ContactEmail
from util.import_contact_emails import generate_contact_emails, import_csv

def test_generate_contact_emails_valid(tmp_path):
    """正常なCSV行から ContactEmail インスタンスが生成されること"""
    csv_content = (
        "その他,Test Content 1,Taro Yamada,たろう やまだ,taro@example.com,男性,192.168.1.1,2025.05.21 09:18:16\n"
        "採用情報について,Test Content 2,Hanako Suzuki,はなこ すずき,hanako@example.com,女性,192.168.1.2,2025.05.22 10:20:30\n"
    )
    csv_file = tmp_path / "valid.csv"
    csv_file.write_text(csv_content, encoding="utf-8")

    emails = list(generate_contact_emails(str(csv_file)))
    assert len(emails) == 2

    email1 = emails[0]
    # 「その他」→ 5, 「男性」→ 1
    assert email1.contact_type == 5
    assert email1.content == "Test Content 1"
    assert email1.name == "Taro Yamada"
    assert email1.kana == "たろう やまだ"
    assert email1.email == "taro@example.com"
    assert email1.gender == 1
    assert email1.ip == "192.168.1.1"
    assert email1.received_at == datetime.strptime("2025.05.21 09:18:16", "%Y.%m.%d %H:%M:%S")

    email2 = emails[1]
    # 「採用情報について」→ 1, 「女性」→ 2
    assert email2.contact_type == 1
    assert email2.content == "Test Content 2"
    assert email2.name == "Hanako Suzuki"
    assert email2.kana == "はなこ すずき"
    assert email2.email == "hanako@example.com"
    assert email2.gender == 2
    assert email2.ip == "192.168.1.2"
    assert email2.received_at == datetime.strptime("2025.05.22 10:20:30", "%Y.%m.%d %H:%M:%S")


def test_generate_contact_emails_invalid(tmp_path, capsys):
    """カラム数不足や不正な変換データがある場合に、その行がスキップされること"""
    csv_content = (
        # 有効な行
        "その他,Valid Content,Taro Yamada,たろう やまだ,taro@example.com,男性,192.168.1.1,2025.05.21 09:18:16\n"
        # カラム不足の行
        "採用情報について,Missing columns\n"
        # 日付フォーマットエラー（正しい形式は YYYY.MM.DD HH:MM:SS）
        "採用情報について,Invalid Date,Name,Kana,email@example.com,男性,192.168.1.2,2025-05-21 09:18:16\n"
        # 不明な性別（"Unknown" はマッピングにない）
        "採用情報について,Invalid Gender,Name,Kana,email@example.com,Unknown,192.168.1.3,2025.05.21 09:18:16\n"
        # 不明な問い合わせ種別（"未知の種別" はマッピングにない）
        "未知の種別,Content,Name,Kana,email@example.com,女性,192.168.1.4,2025.05.21 09:18:16\n"
        # もうひとつ有効な行
        "採用情報について,Valid Content 2,Hanako Suzuki,はなこ すずき,hanako@example.com,女性,192.168.1.5,2025.05.22 10:20:30\n"
    )
    csv_file = tmp_path / "invalid.csv"
    csv_file.write_text(csv_content, encoding="utf-8")

    emails = list(generate_contact_emails(str(csv_file)))
    # 有効な行は1行目と6行目、合計 2 件であるはず
    assert len(emails) == 2

    # 1件目の内容を確認
    email = emails[0]
    assert email.contact_type == 5
    assert email.content == "Valid Content"
    assert email.name == "Taro Yamada"
    assert email.kana == "たろう やまだ"
    assert email.email == "taro@example.com"
    assert email.gender == 1
    assert email.ip == "192.168.1.1"
    assert email.received_at == datetime.strptime("2025.05.21 09:18:16", "%Y.%m.%d %H:%M:%S")

    captured = capsys.readouterr().out
    # エラーの原因となった行のいずれかのエラーメッセージが出力されているはず
    assert ("不正な形式の行をスキップ" in captured) or ("日付フォーマットのエラー" in captured) or ("不明な" in captured)


def test_generate_contact_emails_file_not_found(tmp_path):
    """指定されたCSVファイルが存在しない場合に FileNotFoundError が発生すること"""
    non_existent = tmp_path / "nonexistent.csv"
    with pytest.raises(FileNotFoundError):
        list(generate_contact_emails(str(non_existent)))


def test_import_csv(app, db_session, tmp_path, capsys):
    """CSVファイルから DB へ問い合わせメールが正しくインポートされること"""
    csv_content = (
        "その他,Test Content Taro,John Doe,ジョン ドウ,john@example.com,男性,192.168.1.10,2025.05.20 08:00:00\n"
        "採用情報について,Test Content Hanako,Jane Smith,ジェーン スミス,jane@example.com,女性,192.168.1.11,2025.05.21 09:30:00\n"
    )
    csv_file = tmp_path / "import.csv"
    csv_file.write_text(csv_content, encoding="utf-8")

    # CSV からのインポート
    import_csv(str(csv_file))

    captured = capsys.readouterr().out
    assert "件の問い合わせメールをインポートしました" in captured

    # DB からインポート結果を検証
    emails = ContactEmail.query.all()
    assert len(emails) == 2

    email1 = emails[0]
    # 「その他」→ 5, 「男性」→ 1
    assert email1.contact_type == 5
    assert email1.content == "Test Content Taro"
    assert email1.name == "John Doe"
    assert email1.kana == "ジョン ドウ"
    assert email1.email == "john@example.com"
    assert email1.gender == 1
    assert email1.ip == "192.168.1.10"
    assert email1.received_at == datetime.strptime("2025.05.20 08:00:00", "%Y.%m.%d %H:%M:%S")

    email2 = emails[1]
    # 「採用情報について」→ 1, 「女性」→ 2
    assert email2.contact_type == 1
    assert email2.content == "Test Content Hanako"
    assert email2.name == "Jane Smith"
    assert email2.kana == "ジェーン スミス"
    assert email2.email == "jane@example.com"
    assert email2.gender == 2
    assert email2.ip == "192.168.1.11"
    assert email2.received_at == datetime.strptime("2025.05.21 09:30:00", "%Y.%m.%d %H:%M:%S")
