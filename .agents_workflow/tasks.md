# 問い合わせメール 性別NULL許容対応 タスク

## 1. 事前確認

- [ ] 現在のAlembic最新リビジョンを確認する。
- [ ] `contact_emails.gender` の現行定義が `nullable=False` であることを確認する。
- [ ] 詳細画面の性別表示が `gender` フィルタ経由であることを確認する。

## 2. マイグレーション作成

- [ ] `migrations/versions/` に新規マイグレーションファイルを作成する。
- [ ] `upgrade()` で `contact_emails.gender` を `nullable=True` に変更する。
- [ ] `downgrade()` で `contact_emails.gender` を `nullable=False` に戻す。
- [ ] リビジョンIDと `down_revision` を既存履歴に合わせる。

## 3. モデル変更

- [ ] `app/models.py` の `ContactEmail.gender` を `nullable=True` に変更する。
- [ ] `ContactEmail.gender` の型注釈を `int | None` に変更する。
- [ ] `JobEmail` に不要な変更が入っていないことを確認する。

## 4. CSVインポート変更

- [ ] `util/import_contact_emails.py` の性別変換処理を修正する。
- [ ] 性別列が空白の場合は `gender=None` として扱う。
- [ ] 性別列が `男性` または `女性` の場合は従来通り数値に変換する。
- [ ] 性別列が空白以外の未知値の場合は従来通りスキップする。
- [ ] `kana` の挙動は変更しない。

## 5. 表示確認

- [ ] `gender_filter(None)` が「不明」を返すことを確認する。
- [ ] 問い合わせメール詳細画面で `gender=None` が「不明」と表示されることを確認する。
- [ ] 一覧画面など他に性別表示がないか確認する。

## 6. テスト追加・更新

- [ ] 性別空白の問い合わせメールCSV行がスキップされないテストを追加または更新する。
- [ ] 性別空白の問い合わせメールCSV行が `gender=None` になるテストを追加または更新する。
- [ ] 未知の性別値が従来通りスキップされるテストを維持する。
- [ ] 必要に応じて `gender_filter(None)` または詳細画面表示のテストを追加する。

## 7. 検証

- [ ] 対象テストを実行する。
- [ ] 必要に応じて全テストを実行する。
- [ ] `flask db upgrade` 相当でマイグレーションが適用できることを確認する。
- [ ] `flask db downgrade` 相当の注意点として、NULLデータがある場合は失敗し得ることを確認する。

## 8. 最終確認

- [ ] 変更差分に仕様外の修正が含まれていないことを確認する。
- [ ] `.agents_workflow/requirements.md`、`.agents_workflow/design.md`、`.agents_workflow/tasks.md` の内容と実装が矛盾していないことを確認する。
- [ ] 実行したテスト結果を記録する。
