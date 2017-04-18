import logging
from datetime import datetime

from utils import user, slack, holiday, google_sheets

logger = logging.getLogger(__name__)

# スプレッドシートのID
SHEET_ID = '1u-F1Ixh2s-FBMULHv8w4JrSkQnHsTCG5BjjMQFkWRMU'

def job():
    """
    slack-reminderシートに書いてある通知をSlackに送る
    """

    logger.info('Start slack-reminder job')

    # 休みの日ならなにもしない
    if holiday.is_holiday():
        return

    now = datetime.now()
    # 全データを取得
    values = google_sheets.get_all_values(SHEET_ID, 'reminder')
    for value in values[1:]:
        # TODO: コメント行を無視
        # TODO: 時間をチェック
        # TODO: 日付をチェック
        # TODO: メッセージを送信する
        print(value)
