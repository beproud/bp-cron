from datetime import date

from dateutil import parser

from google_api import get_service
from utils import user, slack, holiday

# カレンダーのID
CALENDAR = {
    'bar': 'beproud.jp_9h9kerkookmotnjmagadgo7j2k@group.calendar.google.com',
    'showroom': 'beproud.jp_qvrqd9512tu4v1jpvf8iek5vco@group.calendar.google.com',
    }

BOT_NAME = '今日の会議室の利用予定'
BOT_EMOJI = ':calendar:'
CHANNEL = '#bp-employees'


def create_message(events):
    """
    今日の予定一覧から slack 送信用のメッセージを作成する

    :param events: イベント情報の辞書
    """
    msg = ""
    result = False
    for room in 'bar', 'showroom':
        # 予定があれば部屋名を追加
        if events[room]:
            result = True
            msg += '*{}*\n'.format(room)
        for event in events[room]:
            msg += '-{start:%H:%M}-{end:%H:%M} {summary}(作成者: {username})\n'.format(**event)
    return msg, result


def job():
    """
    今日の bar, showroom の予定一覧を Slack 通知する
    """
    # 休みの日ならなにもしない
    if holiday.is_holiday():
        return

    # カレンダーAPIに接続
    service = get_service('calendar', 'v3')

    # 検索範囲(今日一杯)を設定
    today = '{:%Y-%m-%d}'.format(date.today())
    time_min = today + 'T00:00:00+09:00'
    time_max = today + 'T23:59:59+09:00'

    events = {}
    for room, calendar_id in CALENDAR.items():
        # 今日のbar, showroomの予定を取得
        event_results = service.events().list(
            calendarId=calendar_id,
            timeMin=time_min,
            timeMax=time_max,
            maxResults=20,
            singleEvents=True,
            orderBy="startTime"
        ).execute()

        # 一覧表示に必要な情報だけを events に入れる
        events[room] = []
        for event in event_results.get('items', []):
            username = user.gaccount_to_slack(event['creator']['email'],
                                              mention=False)
            events[room].append({
                'summary': event['summary'],
                'username': username,
                'start': parser.parse(event['start']['dateTime']),
                'end': parser.parse(event['end']['dateTime']),
            })

    message, result = create_message(events)
    if result:
        slack.post_message(CHANNEL, message, username=BOT_NAME,
                           icon_emoji=BOT_EMOJI)
