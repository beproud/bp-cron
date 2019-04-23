from datetime import datetime, timedelta

from dateutil import parser
from slacker import Error

from src.utils.google_calendar import get_events
from src.utils import user, slack, holiday


# カレンダーのID
CALENDAR = {
    'bar': 'beproud.jp_9h9kerkookmotnjmagadgo7j2k@group.calendar.google.com',
    'showroom': 'beproud.jp_qvrqd9512tu4v1jpvf8iek5vco@group.calendar.google.com',
}

BOT_NAME = '今日の会議室の利用予定'
BOT_EMOJI = ':calendar:'
# CHANNEL = '#bp-employees'
CHANNEL = '#bot-test-wan'


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
            msg += '- {start:%H:%M}-{end:%H:%M} {summary}(作成者: {username})\n'.format(**event)
    return msg, result


def job(event, context):
    """
    今日の bar, showroom の予定一覧を Slack 通知する
    """
    print('Start job')

    # 休みの日ならなにもしない
    if holiday.is_holiday():
        return

    # 検索範囲(今日一杯)を設定
    now = datetime.now()
    time_min = now.replace(hour=0, minute=0, second=0)
    time_max = now.replace(hour=23, minute=59, second=59)

    events = {}
    for room, calendar_id in CALENDAR.items():
        # 一覧表示に必要な情報だけを events に入れる
        events[room] = []

        # 今日のbar, showroomの予定を取得
        for event in get_events(calendar_id, time_min, time_max):
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

    print('End job')


def _send_next_meeting_message(room, event):
    """
    次のミーティング情報を Slack で送信する

    :param str room: 部屋の名前(bar, showroom)
    :param event: イベント情報
    https://developers.google.com/google-apps/calendar/v3/reference/events
    """
    location = event['location']
    start = parser.parse(event['start']['dateTime'])
    end = parser.parse(event['end']['dateTime'])
    summary = event['summary']
    # 参加者の一覧を生成
    attendees = []
    for attendee in event.get('attendees', []):
        email = attendee['email']
        if 'group.calendar.google.com' not in email:
            username = user.gaccount_to_slack(attendee['email'], mention=False)
            attendees.append(username)

    # メッセージのアタッチメントを作成
    # https://api.slack.com/docs/message-attachments
    attachments = [{
        "fields": [
            {
                "title": "場所",
                "value": room,
                "short": True
            },
            {
                "title": "時間",
                "value": '{:%H:%M}〜{:%H:%M}'.format(start, end),
                "short": True,
            },
            {
                "title": "参加者",
                "value": ', '.join(attendees),
                "short": True,
            }
        ],
    }]
    try:
        slack.post_message(location, summary, attachments=attachments,
                           username=BOT_NAME, icon_emoji=BOT_EMOJI)
    except Error:
        # チャンネルが存在しない場合はエラーになるので無視する
        pass


def recent(event, context):
    """
    指定した時間の範囲にあるミーティング予定を Slack 通知する

    :param int minutes: 何分後までを対象とするか(default: 15分)
    """
    print('Start next_meeting')

    # 休みの日ならなにもしない
    if holiday.is_holiday():
        return

    # 検索範囲(現在時刻から minutes 分後まで)を設定
    # TODO: 固定値にしていいかtakanoryさんに確認
    now = datetime.now()
    time_max = now + timedelta(minutes=15)

    for room, calendar_id in CALENDAR.items():
        # 指定範囲内のbar, showroomの予定を取得
        for event in get_events(calendar_id, now, time_max):
            # 場所が指定してあったら、その slack channel に通知する
            if 'location' in event:
                _send_next_meeting_message(room, event)
