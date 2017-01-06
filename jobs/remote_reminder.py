import gspread
from datetime import datetime

from google_api import get_credentials

from utils import user, slack

# スプレッドシートのID
SHEET_ID = '1VHHJDj-AVmQypSDIBHswNJrPV6RAQVSo3FG7lbMUSmc'

BOT_NAME = '本日のリモート勤務一覧'
BOT_EMOJI = (':clock8:', ':clock1230:')
CHANNEL = '#bp-remote'


def create_message(google_accounts):
    """
    本日のリモート勤務一覧用のメッセージを作成する

    :param google_accounts: リモート勤務予定者のGoogleアカウントのリスト
    """
    message = '{:%Y/%m/%d %H:%M:%S}\n'.format(datetime.now())
    if google_accounts:
        users = (user.gaccount_to_slack(ga) for ga in google_accounts)
        message += ", ".join(users)
    else:
        message += '本日は自宅作業の申請はありません。'
    return message


def job(morning=False):
    """
    リモート勤務の人の一覧を通知する

    :param morning: True の場合朝のメッセージ(メンション付き)となる
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
    google_accounts = []
    for row in ws.get_all_values():
        if row[2] == today:
            google_accounts.append(row[1])

    message = create_message(google_accounts)

    # 朝の場合は絵文字を変えて、メンションする
    if morning:
        slack.post_message(CHANNEL, message, username=BOT_NAME,
                           icon_emoji=BOT_EMOJI[0], link_names=True)
    else:
        slack.post_message(CHANNEL, message, username=BOT_NAME,
                           icon_emoji=BOT_EMOJI[1])
