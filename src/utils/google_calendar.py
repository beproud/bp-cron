from src.utils.google_api import get_service


def _get_time_str(datetime_):
    """
    日付を Google の Calendar API が扱う形式の文字列に変換する

    :param datetime datetime_: 日時
    """
    # マイクロ秒を削除
    datetime_ = datetime_.replace(microsecond=0)
    datetime_str = datetime_.isoformat()
    if datetime_.tzinfo is None:
        datetime_str += '+09:00'  # タイムゾーンの文字列を加える
    return datetime_str


def get_events(calendar_id, time_min, time_max):
    """
    任意のカレンダーの指定範囲にあるイベントの一覧を返す

    * https://developers.google.com/google-apps/calendar/v3/reference/events/list
    * https://developers.google.com/resources/api-libraries/documentation/calendar/v3/python/latest/calendar_v3.events.html#list

    :param str calendar_id: カレンダーID
    :param datetime time_min: 検索範囲の開始日時
    :param datetime time_max: 検索範囲の終了日時
    """
    # カレンダーAPIに接続
    service = get_service('calendar', 'v3')

    # 指定したカレンダーにある指定範囲のイベントを取得する
    event_results = service.events().list(
        calendarId=calendar_id,
        timeMin=_get_time_str(time_min),  # 日時を文字列にする
        timeMax=_get_time_str(time_max),
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    events = event_results.get('items', [])

    return events
