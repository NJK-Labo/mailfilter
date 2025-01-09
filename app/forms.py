from flask_wtf import FlaskForm  # type: ignore
from wtforms import Form  # type: ignore
from wtforms.fields import DateField, SearchField, SelectField, SubmitField  # type: ignore
from wtforms.validators import Length, Optional, ValidationError  # type: ignore


def validate_select(form, field):
    """問い合わせ種別のバリデーション関数"""
    if field.data not in ["1", "2", "3", "4", "5"]:
        raise ValidationError("不正な問い合わせ種別です。")


class ContactEmailSearchForm(FlaskForm):
    """問い合わせメール一覧の検索フォームクラス"""

    class Meta:
        csrf = False  # 検索に使うだけなのでCSRFトークンを無効化

    keyword = SearchField(
        "検索キーワード入力項目",
        render_kw={"placeholder": "検索キーワード"},
        validators=[Optional(), Length(max=255, message="検索キーワードは255文字以内で入力してください。")],
    )
    start_date = DateField("検索対象期間（開始）", format="%Y-%m-%d", validators=[Optional()])
    end_date = DateField("検索対象期間（終了）", format="%Y-%m-%d", validators=[Optional()])

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
        validators=[Optional(), validate_select],
    )
    search = SubmitField("検索")


class JobEmailSearchForm(Form):
    """求人関係メール一覧の検索フォームクラス"""

    class Meta:
        csrf = False  # 検索に使うだけなのでCSRFトークンを無効化

    keyword = SearchField(
        "検索キーワード入力項目",
        render_kw={"placeholder": "検索キーワード"},
        validators=[Optional(), Length(max=255, message="検索キーワードは255文字以内で入力してください。")],
    )
    start_date = DateField("検索対象期間（開始）", format="%Y-%m-%d", validators=[Optional()])
    end_date = DateField("検索対象期間（終了）", format="%Y-%m-%d", validators=[Optional()])

    search = SubmitField("検索")
