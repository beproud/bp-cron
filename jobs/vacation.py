import logging
from datetime import date
from enum import IntEnum

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


class OldColInfo(IntEnum):
    """
    旧シートの列情報

    TODO: 将来的に削除する
    """
    email = 1   # メールアドレス
    target = 3  # 休みの対象日
    vtype = 4   # 休みの種類
    time = 6    # 時間休の時間


class ColInfo(IntEnum):
    """
    新シートの列情報
    """
    email = 1   # メールアドレス
    target = 2  # 休みの対象日
    vtype = 5   # 休みの種類
    time = 6    # 時間休の時間


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


def _get_vacation_list_from_old_sheet(worksheet, today):
    """
    旧シートから指定された日付が休みの人の一覧を取得する

    :param worksheet: Google Spreadsheet の任意のワークシート
    :param today: 今日を表す文字列(YYYY/MM/DD)
    """
    vacation_list = []

    # 日付が今日の申請者一覧を取得
    for row in worksheet.get_all_values():
        if row[OldColInfo.target] == today:
            name = user.gaccount_to_slack(row[OldColInfo.email], mention=False)
            type_str = _get_type_str(row[OldColInfo.vtype])
            if type_str == '時間休':
                name += '({})'.format(row[OldColInfo.time])
            vacation_list.append((type_str, name))

    return vacation_list


def _get_vacation_list_from_sheet(worksheet, today):
    """
    旧シートから指定された日付が休みの人の一覧を取得する

    :param worksheet: Google Spreadsheet の任意のワークシート
    :param today: 今日を表す文字列(YYYY/MM/DD)
    """
    vacation_list = []

    # 日付が今日の申請者一覧を取得
    for row in worksheet.get_all_values():
        if row[ColInfo.target] == today:
            name = user.gaccount_to_slack(row[ColInfo.email], mention=False)
            type_str = _get_type_str(row[ColInfo.vtype])
            if type_str == '時間休':
                name += '({}時間)'.format(row[ColInfo.time])
            vacation_list.append((type_str, name))

    return vacation_list


def _create_message(vacation_list):
    """
    休みの人の一覧情報から slack での送信用のメッセージを作成する

    :param vacation_list: 休みの人のリスト。下記の形式で入っている
        `[('全休', 'takanory'), ('時間休', 'masaya(1時間))]
    """
    message = ''
    for vtype in VACATION_TYPE:
        # 指定の休みの人リストを取得
        members = [v[1] for v in vacation_list if v[0] == vtype]
        if members:
            message += '- {}: {}\n'.format(vtype, ', '.join(members))

    return message


def daily():
    """
    今日の休みの人の一覧をSlackに通知する
    """
    logger.info('Start daily job')

    # 休みの日ならなにもしない
    if holiday.is_holiday():
        return

    # 今日の日付
    today = '{:%Y/%m/%d}'.format(date.today())

    # 結果を保存する領域
    vacation = {}
    for vtype in VACATION_TYPE:
        vacation[vtype] = []

    # 認証処理
    credentials = get_credentials()
    gc = gspread.authorize(credentials)

    # 新シートから休みの人の情報を取得
    sheet = gc.open_by_key(SHEET_ID)
    ws = sheet.worksheet('master')
    vacation_list = _get_vacation_list_from_sheet(ws, today)

    # 旧シートから休みの人の情報を取得
    # TODO: 将来的に削除する
    sheet = gc.open_by_key(OLD_SHEET_ID)
    ws = sheet.worksheet('master')
    vacation_list.extend(_get_vacation_list_from_old_sheet(ws, today))

    # 休みの人一覧からメッセージを生成して送信
    message = _create_message(vacation_list)
    if message:
        slack.post_message(CHANNEL, message, username=BOT_NAME,
                           icon_emoji=BOT_EMOJI)

    logger.info('End daily job')
