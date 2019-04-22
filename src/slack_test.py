from slacker import Slacker
import settings

BOT_NAME = '誕生日'
BOT_EMOJI = ':birthday:'
CHANNEL = '#bot-test-wan'


def post_message(channel, text, username=None, link_names=None,
                 attachments=None, icon_emoji=None):
    """
    指定したパラメーターでSlackにメッセージを送信する

    :param channel: チャンネル名
    :param text: 送信するメッセージのテキスト
    :param username: 表示されるユーザー名
    :param link_names: True に設定するとメンションが有効になる
    :param attachments: メッセージのアタッチメント
    :param icon_emoji: ユーザーのアイコン
    """
    print('Slack post message: channel=%s', channel)
    if not username:
        username = settings.BOT_NAME
    if not icon_emoji:
        icon_emoji = settings.BOT_EMOJI
    if settings.DEBUG and settings.DEBUG_CHANNEL:
        channel = settings.DEBUG_CHANNEL

    # slack にメッセージを送信する
    slack = Slacker(settings.SLACK_TOKEN)
    slack.chat.post_message(channel, text,
                            username=username,
                            link_names=link_names,
                            attachments=attachments,
                            icon_emoji=icon_emoji)


def main(event, context):
    """
    今日誕生日の人を通知する
    """
#     slack = Slacker(settings.SLACK_TOKEN)
    print('Start job')
    post_message(CHANNEL, "test", username=BOT_NAME, icon_emoji=BOT_EMOJI)
    print('End job')
