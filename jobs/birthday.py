from datetime import date
from random import choice

from google_api import get_service
from utils import slack

# カレンダーのID
CALENDAR_ID = 'beproud.jp_njbpgdq8kq419opf2eq8n7njnc@group.calendar.google.com'

# メッセージに追加する絵文字リスト
EMOJI = ('beer', 'beers', 'tada', 'confetti_ball')

BOT_NAME = '誕生日'
BOT_EMOJI = ':birthday:'
CHANNEL = '#random'


def job():
    """
    今日誕生日の人を通知する
    """
    today = '{:%Y-%m-%d}'.format(date.today())
    time_min = today + 'T00:00:00+09:00'
    time_max = today + 'T23:59:59+09:00'

    # カレンダーAPIに接続
    service = get_service('calendar', 'v3')
    # 誕生日カレンダーにある今日の予定を取得する
    event_results = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=time_min,
        timeMax=time_max,
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    msg = ''
    for event in event_results.get('items', []):
        msg += '今日は {} です :{}:'.format(event['summary'], choice(EMOJI))

    if msg:
        slack.post_message(CHANNEL, msg, username=BOT_NAME,
                           icon_emoji=BOT_EMOJI)
