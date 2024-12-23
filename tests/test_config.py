from datetime import datetime

from config import Config


def test_now_jst():
    """JST時刻を返すかどうか"""
    now = Config.now_jst()
    assert now.tzinfo.zone == "Asia/Tokyo"
    assert isinstance(now, datetime)
