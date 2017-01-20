import logging
from datetime import datetime
from random import choice

from utils.google_calendar import get_events
from utils import slack

logger = logging.getLogger(__name__)

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
    logger.info('Start job')

    # 今日の0時から23時までを範囲とする
    now = datetime.now()
    time_min = now.replace(hour=0, minute=0, second=0, microsecond=0)
    time_max = now.replace(hour=23, minute=59, second=49, microsecond=0)

    # カレンダーからイベントを取得する

    msg = ''
    for event in get_events(CALENDAR_ID, time_min, time_max):
        msg += '今日は {} です :{}:'.format(event['summary'], choice(EMOJI))

    if msg:
        slack.post_message(CHANNEL, msg, username=BOT_NAME,
                           icon_emoji=BOT_EMOJI)

    logger.info('End job')
