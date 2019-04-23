from datetime import datetime

from src.utils import user, slack, google_sheets

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


def morning_job(event, context):
    job(morning=True)


def night_job(event, context):
    job()


def job(morning=False):
    """
    リモート勤務の人の一覧を通知する

    :param morning: True の場合朝のメッセージ(メンション付き)となる
    """
    print('Start job')

    # 今日の日付
    today = '{:%Y/%m/%d}'.format(datetime.now())

    # スプレッドシートの指定のシートのデータを取得
    values = google_sheets.get_all_values(SHEET_ID, 'master')

    # 日付が今日の申請者一覧を取得
    google_accounts = []
    for row in values:
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

    print('End job')
