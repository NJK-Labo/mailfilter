def contact_type_filter(value):
    """contact_type を数値から対応する名前に変換する"""
    mapping = {
        1: "採用情報について",
        2: "取り扱い製品について",
        3: "事業内容について",
        4: "プライバシーポリシーについて",
        5: "その他",
    }
    return mapping.get(value, "不明")
