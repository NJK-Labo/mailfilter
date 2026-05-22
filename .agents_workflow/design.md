# 問い合わせメール 性別NULL許容対応 設計

## 方針

問い合わせメールの性別（`contact_emails.gender`）だけをNULL許容にする。
CSVで性別が空白の場合は `NULL` として保存し、画面表示では既存の性別フィルタを通して「不明」と表示する。

`kana` は現状通り空文字として扱い、DB定義は変更しない。

## 変更対象

### マイグレーション

新規マイグレーションファイルを `migrations/versions/` に追加する。

- `upgrade()`
  - `contact_emails.gender` を `nullable=True` に変更する。
- `downgrade()`
  - `contact_emails.gender` を `nullable=False` に戻す。

既存マイグレーションでは `op.batch_alter_table()` が使われているため、同じ形式にそろえる。

想定コード:

```python
with op.batch_alter_table("contact_emails", schema=None) as batch_op:
    batch_op.alter_column(
        "gender",
        existing_type=sa.Integer(),
        nullable=True,
    )
```

`downgrade()` では `nullable=False` に戻す。ただし、DB内に `gender IS NULL` のレコードが残っている状態ではDBによって失敗する可能性がある。必要なら運用時にNULLデータを補正してからダウングレードする。

### モデル

`app/models.py` の `ContactEmail.gender` をNULL許容に変更する。

- 現状: `gender: int = db.Column(db.Integer, nullable=False)`
- 変更後: `gender: int | None = db.Column(db.Integer, nullable=True)`

`JobEmail` は変更しない。

### CSVインポート

`util/import_contact_emails.py` の性別変換処理を変更する。

処理方針:

1. `gender_str.strip()` を変数に入れる。
2. 空文字の場合は `gender = None` にする。
3. 空文字でない場合は `GENDER_MAPPING` で変換する。
4. 変換できない未知の値は従来通りスキップする。

想定ロジック:

```python
gender_value = gender_str.strip()
if gender_value == "":
    gender = None
else:
    gender = GENDER_MAPPING.get(gender_value)
    if gender is None:
        print(f"不明な性別をスキップ: {gender_str}")
        continue
```

問い合わせ種別、受信日時、その他項目の挙動は変更しない。

### 表示

`app/templates/show_contact_email.html` は既に `{{mail.gender | gender}}` を使っている。

`util/constants.py` の `gender_filter()` は `GENDER_INVERSE.get(value, "不明")` のため、`None` を渡すと「不明」を返す。詳細画面は追加変更なしで要件を満たせる見込み。

一覧画面に性別表示が追加されていないため、現時点では詳細画面のみ確認対象とする。

### テスト

既存の `tests/util/test_import_contact_emails.py` を更新する。

追加・更新する観点:

- 性別が空白のCSV行で `ContactEmail` が生成される。
- 生成された `ContactEmail.gender` が `None` になる。
- `import_csv()` 実行後、DB上の `gender` が `None` で保存される。
- 性別が未知の文字列の場合は従来通りスキップされる。

表示については既存の詳細画面テスト、またはフィルタテストで確認する。

- `gender_filter(None)` が「不明」を返すこと。
- 必要なら `tests/test_routes.py` に、`gender=None` の問い合わせメール詳細で「不明」が含まれることを追加する。

## 影響範囲

- 問い合わせメールCSVインポートで、これまでスキップされていた性別空白行が登録される。
- 性別がNULLの問い合わせメールがDBに存在するようになる。
- 詳細画面では性別NULLが「不明」と表示される。
- `gender` を整数前提で直接扱う処理がある場合は、`None` を考慮する必要がある。

## 非対象

- `kana` のNULL許容化。
- 求人関連メールの変更。
- 性別の新しい区分値追加。
- 過去にスキップされたCSV行の再投入やデータ復旧。
