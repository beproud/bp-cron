from datetime import datetime

from slacker import Slacker

import settings

def time_signal():
    """
    時間を通知するjob
    """
    slack = Slacker(settings.SLACK_TOKEN)
    slack.chat.post_message('#bot-test-takanory', datetime.now().isoformat())
    print(datetime.now().isoformat())
