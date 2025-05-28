"""各種定数および変換マッピング・フィルタ処理をまとめたモジュール"""

# 問い合わせ種別の文字列⇄数値のマッピング
CONTACT_TYPE_MAPPING = {
    "採用情報について": 1,
    "取り扱い製品について": 2,
    "事業内容について": 3,
    "プライバシーポリシーについて": 4,
    "その他": 5,
}

# 数値から問い合わせ種別の文字列への逆引きマッピング（フィルタ等で利用）
CONTACT_TYPE_INVERSE = {v: k for k, v in CONTACT_TYPE_MAPPING.items()}

# 性別の文字列⇄数値のマッピング
GENDER_MAPPING = {
    "男性": 1,
    "女性": 2,
}

# 数値から性別の文字列への逆引きマッピング（フィルタ等で利用）
GENDER_INVERSE = {v: k for k, v in GENDER_MAPPING.items()}

def contact_type_filter(value):
    """
    問い合わせ種別の数値を文字列に変換するフィルタ関数
    
    :param value: 数値（1～5）の問い合わせ種別
    :return: 対応する問い合わせ種別の名称。見つからなければ "不明" を返す
    """
    return CONTACT_TYPE_INVERSE.get(value, "不明")

def gender_filter(value):
    """
    性別の数値を文字列に変換するフィルタ関数
    
    :param value: 数値（1または2）の性別
    :return: 対応する性別の名称。見つからなければ "不明" を返す
    """
    return GENDER_INVERSE.get(value, "不明")
