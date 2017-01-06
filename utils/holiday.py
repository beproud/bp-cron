import logging
from datetime import datetime, date, timedelta

from dateutil import parser
from dateutil.rrule import rrule, DAILY

from google_api import get_service

logger = logging.getLogger(__name__)

# 日本の祝日カレンダー
CALENDAR_ID = 'ja.japanese#holiday@group.v.calendar.google.com'

# 日本の祝日を入れておくセット
holiday_set = set()

# 年末年始休暇の開始日と終了日
START = date(2016, 12, 29)
END = date(2017, 1, 4)


def update_japanese_holiday():
    """
    日本の祝日情報を更新する
    """
    logger.info('Update japanese holiday')
    # 中身をクリアする
    holiday_set.clear()

    # 年末年始休暇を設定
    newyear_rule = rrule(freq=DAILY, dtstart=START, until=END)
    holiday_set.update(x.date() for x in newyear_rule)

    # カレンダーの検索範囲は今日から一年後まで
    today = date.today()
    next_year = today + timedelta(days=365)
    today_str = '{:%Y-%m-%d}T00:00:00+09:00'.format(today)
    next_year_str = '{:%Y-%m-%d}T00:00:00+09:00'.format(next_year)
    # カレンダーAPIに接続
    service = get_service('calendar', 'v3')

    # 日本の祝日カレンダーにある予定を取得する
    event_results = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=today_str,
        timeMax=next_year_str
    ).execute()
    for event in event_results.get('items', []):
        holiday = parser.parse(event['start']['date']).date()
        holiday_set.add(holiday)


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

    # 日本の祝日カレンダーで祝日なら True を返す
    if date_data in holiday_set:
        return True

    return False


# 日本の祝日情報を初期化する
update_japanese_holiday()
