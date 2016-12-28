from slacker import Slacker

import settings


def post_message(channel, message, username=None, icon_emoji=None,
                 link_names=None):
    """
    指定したパラメーターでSlackにメッセージを送信する

    :param channel: チャンネル名
    :param message: 送信するメッセージ
    :param username: 表示されるユーザー名
    :param icon_emoji: ユーザーのアイコン
    :param link_names: True に設定するとメンションが有効になる
    """
    if not username:
        username = settings.BOT_NAME
    if not icon_emoji:
        icon_emoji = settings.BOT_EMOJI
    if settings.DEBUG and settings.DEBUG_CHANNEL:
        channel = settings.DEBUG_CHANNEL

    # slack にメッセージを送信する
    slack = Slacker(settings.SLACK_TOKEN)
    slack.chat.post_message(channel, message,
                            username=username,
                            icon_emoji=icon_emoji,
                            link_names=link_names)
