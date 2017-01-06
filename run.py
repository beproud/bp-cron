import logging
import time

import schedule

from jobs import remote_reminder, meeting_reminder, birthday
from utils.holiday import update_japanese_holiday

logger = logging.getLogger(__name__)


def main():
    logger.info('Set schedule')
    # https://project.beproud.jp/redmine/projects/bptools/wiki/slack-bot
    # 0:30 くらいにリモート勤務一覧
    schedule.every().day.at('0:30').do(remote_reminder.job)
    # 8:30 くらいにリモート勤務一覧(メンション付き)
    schedule.every().day.at('8:30').do(remote_reminder.job, True)
    # 5分毎にslack-reminder
    # schedule.every(5).minutes.do(slack_reminder)
    # 9:00 くらいにカレンダーからミーティング一覧通知
    schedule.every().day.at('9:00').do(meeting_reminder.job)
    # 15分ごとにミーティング予定を通知
    # schedule.every(15).minutes.do(meeting_notify)
    # 水曜の9時くらいにカイゼンミーティングを通知
    # schedule.every().wednesday.at("9:00").do(kaizen_notify)
    # schedule.every().wednesday.at("17:00").do(kaizen_notify)
    # 誕生日通知
    schedule.every().day.at('9:30').do(birthday.job)
    # BPBP購入通知
    # 休みの人通知
    # 9:30 くらいに休みの人を通知
    # schedule.every().day.at("9:30").do(holiday)
    # 30日ごとに祝日カレンダーを更新する
    schedule.every(30).days.do(update_japanese_holiday)

    logger.info('Start schedule')
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
