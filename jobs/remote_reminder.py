import gspread
from datetime import datetime

from slacker import Slacker
from google_api import get_credentials

import settings

# スプレッドシートのID
SHEET_ID = '1VHHJDj-AVmQypSDIBHswNJrPV6RAQVSo3FG7lbMUSmc'

BOT_NAME = '本日のリモート勤務一覧'


def create_message(users):
    """
    本日のリモート勤務一覧用のメッセージを作成する
    """
    message = '{:%Y/%m/%d %H:%M:%S}\n'.format(datetime.now())
    if users:
        message += ", ".join(users)
    else:
        message += '本日は自宅作業の申請はありません。'
    return message


def job():
    """
    リモート勤務の人の一覧を通知する
    """
    # 今日の日付
    today = '{:%Y/%m/%d}'.format(datetime.now())

    # 認証処理
    credentials = get_credentials()
    gc = gspread.authorize(credentials)

    # スプレッドシートの任意のワークシートを開く
    sheet = gc.open_by_key(SHEET_ID)
    ws = sheet.worksheet('master')

    # 日付が今日の申請者一覧を取得
    users = []
    for row in ws.get_all_values():
        if row[2] == today:
            users.append(row[1])

    message = create_message(users)

    # slackで通知
    slack = Slacker(settings.SLACK_TOKEN)
    # :clock8'
    slack.chat.post_message('#bot-test-takanory', message,
                            username=BOT_NAME,
                            icon_emoji=':clock1230:',
                            link_names=True)
