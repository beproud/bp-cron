import logging
from datetime import date

import gspread
from google_api import get_credentials

from utils import user, slack, holiday

logger = logging.getLogger(__name__)

# スプレッドシートのID
OLD_SHEET_ID = '1v-Asl9Lt8RAddTaCMSwrQZe1csDePvtdnzSetEg9F8E'
SHEET_ID = '11N3HudIAvn7sKTrMpu_CHYPXFK8L-SBa3AogL6kH96s'

BOT_NAME = '本日のお休み一覧'
BOT_EMOJI = ':palm_tree:'
CHANNEL = '#general'
VACATION_TYPE = ('全休', '午前半休', '午後半休', '時間休')


def _get_type_str(type_str):
    """
    休みの種別の文字列を返す

    :param str type_str: 午後半休（14：00~18：00）などが入ってくる
    """
    for vtype in VACATION_TYPE:
        if vtype in type_str:
            # 種別を上書きする
            type_str = vtype
            break
    return type_str


def _get_vacation_list_from_old_sheet(gc, today):
    """
    旧シートから指定された日付が休みの人の一覧を取得する

    :param gc: Google Spreadshhet へのアクセス用のインスタンス
    :param today: 今日を表す文字列(YYYY/MM/DD)
    """
    vacation_list = []

    # スプレッドシートの任意のワークシートを開く
    sheet = gc.open_by_key(OLD_SHEET_ID)
    ws = sheet.worksheet('master')

    # 日付が今日の申請者一覧を取得
    for row in ws.get_all_values():
        if row[3] == today:
            name = user.gaccount_to_slack(row[1], mention=False)
            type_str = _get_type_str(row[4])
            if type_str == '時間休':
                name += '({})'.format(row[6])
            vacation_list.append((type_str, name))

    return vacation_list


def _get_vacation_list_from_sheet(gc, today):
    """
    旧シートから指定された日付が休みの人の一覧を取得する

    :param gc: Google Spreadshhet へのアクセス用のインスタンス
    :param today: 今日を表す文字列(YYYY/MM/DD)
    """
    vacation_list = []

    # スプレッドシートの任意のワークシートを開く
    sheet = gc.open_by_key(SHEET_ID)
    ws = sheet.worksheet('master')

    # 日付が今日の申請者一覧を取得
    for row in ws.get_all_values():
        if row[2] == today:
            name = user.gaccount_to_slack(row[1], mention=False)
            type_str = _get_type_str(row[5])
            if type_str == '時間休':
                name += '({}時間)'.format(row[6])
            vacation_list.append((type_str, name))

    return vacation_list


def daily():
    """
    今日の休みの人の一覧をSlackに通知する
    """
    logger.info('Start job')

    # 休みの日ならなにもしない
    if holiday.is_holiday():
        return

    # 今日の日付
    today = '{:%Y/%m/%d}'.format(date.today())
    today = '2017/01/23'

    # 結果を保存する領域
    vacation = {}
    for vtype in VACATION_TYPE:
        vacation[vtype] = []

    # 認証処理
    credentials = get_credentials()
    gc = gspread.authorize(credentials)

    # 旧シートから休みの人の情報を取得
    vacation_list = _get_vacation_list_from_old_sheet(gc, today)
    # 新シートから休みの人の情報を取得
    vacation_list.extend(_get_vacation_list_from_sheet(gc, today))

    print(vacation_list)

    # message = create_message(google_accounts)

    logger.info('End job')
