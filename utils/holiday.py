from datetime import datetime, date

from dateutil import parser


def is_holiday(date_data=date.today()):
    """
    指定された日付が休日かどうかを返す

    :param date: 日付(文字列、datetime、date型のいずれか)
    :reutrn: True - 祝日、False - 平日
    """
    if isinstance(date_data, datetime):
        # datetime は date に変換する
        date_data = date_data.date()
    elif isinstance(date_data, str):
        # 文字列の場合も date に変換する
        date_data = parser.parse(date_data).date()
    elif not isinstance(date_data, date):
        # TODO: 日付以外の場合は例外を返す予定
        return False

    # 土日だったら True を返す
    if date_data.weekday() in (5, 6):
        return True

    # TODO: カレンダーで祝日なら True を返す

    # TODO: 年末年始休暇なら True を返す
    
    return False
