DEBUG = False

BOT_EMOJI = ':robot_face:'
BOT_NAME = 'bp-cron'


try:
    from src.bpcron_settings import * # NOQA
except:
    pass
