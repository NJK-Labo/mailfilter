from flask_wtf import FlaskForm  # type: ignore
from wtforms import Form  # type: ignore
from wtforms.fields import DateField, SearchField, SelectField, SubmitField  # type: ignore


class ContactEmailSearchForm(FlaskForm):
    """問い合わせメール一覧の検索フォームクラス"""

    keyword = SearchField("検索キーワード入力項目", render_kw={"placeholder": "検索キーワード"})
    start_date = DateField("検索対象期間（開始）", format="%Y-%m-%d")
    end_date = DateField("検索対象期間（終了）", format="%Y-%m-%d")
    type = SelectField(
        "問い合わせ種別",
        choices=[
            ("", "-- 問い合わせ種別 --"),  # 初期値
            ("1", "採用情報について"),
            ("2", "取り扱い製品について"),
            ("3", "事業内容について"),
            ("4", "プライバシーポリシーについて"),
            ("5", "その他"),
        ],
        default="",
    )
    search = SubmitField("検索")


class JobEmailSearchForm(Form):
    """求人関係メール一覧の検索フォームクラス"""

    keyword = SearchField("検索キーワード入力項目", render_kw={"placeholder": "検索キーワード"})
    start_date = DateField("検索対象期間（開始）", format="%Y-%m-%d")
    end_date = DateField("検索対象期間（終了）", format="%Y-%m-%d")

    search = SubmitField("検索")
