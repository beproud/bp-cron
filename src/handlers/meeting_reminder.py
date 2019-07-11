import logging
from datetime import datetime, timedelta

from dateutil import parser, tz
from slacker import Error

from src.utils import holiday, slack, user
from src.utils.google_calendar import get_events

BAR = "bar(20)"
SHOWROOM = "showroom(5)"
MADOGIWA = "madogiwa(6)"
ZOOM_TAKANORY = "Zoom takanory(100)"

# カレンダーのID
CALENDAR = {
    BAR: "beproud.jp_1883iqgkfa6esi3cmvg49h2i9clna6gb6cs3gd9n60s32d9l6g@resource.calendar.google.com",  # NOQA
    SHOWROOM: "beproud.jp_1886bcjnjrs50j20ip16ufnpap2io6ga68q3adpp64qj4d1k@resource.calendar.google.com",  # NOQA
    MADOGIWA: "beproud.jp_188bk12tilr6cjdlh321lefu6me0i6gb68rj4dpn70q36cpo6o@resource.calendar.google.com",  # NOQA
    ZOOM_TAKANORY: "beproud.jp_188bcfric73vejvqim1abu7mkaa9i6gb64oj6e9m6gq3ge9n60@resource.calendar.google.com",  # NOQA
}

BOT_EMOJI = ":calendar:"
CHANNEL = "#bp-employees"

logger = logging.getLogger()


def create_message(events):
    """
    今日の予定一覧から slack 送信用のメッセージを作成する

    :param events: イベント情報の辞書
    """
    msg = ""
    result = False
    for room in BAR, SHOWROOM, MADOGIWA, ZOOM_TAKANORY:
        # 予定があれば部屋名を追加
        if events[room]:
            result = True
            msg += "*{}*\n".format(room)
        for event in events[room]:
            msg += "- {start:%H:%M}-{end:%H:%M} {summary}(作成者: {username})\n".format(
                **event
            )
    return msg, result


def job(event, context):
    """
    今日の bar, showroom, madogiwa, zoom_takanory の予定一覧を Slack 通知する
    """
    logger.info("Start job")

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
            username = user.gaccount_to_slack(event["creator"]["email"], mention=False)
            events[room].append(
                {
                    "summary": event["summary"],
                    "username": username,
                    "start": parser.parse(event["start"]["dateTime"]),
                    "end": parser.parse(event["end"]["dateTime"]),
                }
            )

    message, result = create_message(events)
    if result:
        slack.post_message(
            CHANNEL, message, username="今日の会議室の利用予定", icon_emoji=BOT_EMOJI
        )

    logger.info("End job")


def _send_next_meeting_message(room, event, channel):
    """
    次のミーティング情報を Slack で送信する

    :param str room: 部屋の名前(bar, showroom, madogiwa, zoom_takanory)
    :param event: イベント情報
    :param channel: POSTするSlackチャンネル
    https://developers.google.com/google-apps/calendar/v3/reference/events
    """
    start = parser.parse(event["start"]["dateTime"])
    end = parser.parse(event["end"]["dateTime"])
    summary = event["summary"]
    # 参加者の一覧を生成
    attendees = []
    for attendee in event.get("attendees", []):
        email = attendee["email"]
        # 参加者情報からカレンダーを除去
        if "resource.calendar.google.com" not in email:
            username = user.gaccount_to_slack(attendee["email"], mention=False)
            attendees.append(username)

    # メッセージのアタッチメントを作成
    # https://api.slack.com/docs/message-attachments
    attachments = [
        {
            "fields": [
                {"title": "場所", "value": room, "short": True},
                {
                    "title": "時間",
                    "value": "{:%H:%M}〜{:%H:%M}".format(start, end),
                    "short": True,
                },
                {"title": "参加者", "value": ", ".join(attendees), "short": True},
            ]
        }
    ]
    try:
        slack.post_message(
            channel,
            summary,
            attachments=attachments,
            username="Calendar bot",
            icon_emoji=BOT_EMOJI,
            link_names=True,
        )
    except Error:
        # チャンネルが存在しない場合はエラーになるので無視する
        pass


def is_send_message(event):
    """Slackに送信可能なeventかチェックする

    :param events: イベント情報の辞書
    """
    channel = None
    location = event["location"]
    start = parser.parse(event["start"]["dateTime"])
    if "location" not in event:
        return channel, False
    now = datetime.now(tz.gettz("Asia/Tokyo"))
    # 開始時刻が現在時刻より前のイベントを対象にする
    if now > start:
        return channel, False
    # Slackチャンネルを特定
    for loc in location.split(","):
        if loc.startswith("#"):
            channel = loc
            break
    if not channel:
        return channel, False
    return channel, True


def recent(event, context):
    """
    指定した時間の範囲にあるミーティング予定を Slack 通知する
    """
    logger.info("Start next_meeting")

    # 休みの日ならなにもしない
    if holiday.is_holiday():
        return

    # 検索範囲(現在時刻から 15 分後まで)を設定
    now = datetime.now()
    time_max = now + timedelta(minutes=15)

    for room, calendar_id in CALENDAR.items():
        # 指定範囲内のbar, showroomの予定を取得
        for event in get_events(calendar_id, now, time_max):
            channel, is_send = is_send_message(event)
            if is_send:
                _send_next_meeting_message(room, event, channel)
