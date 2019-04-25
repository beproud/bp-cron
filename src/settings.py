DEBUG = True

BOT_EMOJI = ':robot_face:'
BOT_NAME = 'bp-cron'


try:
    from bpcron_settings import * # NOQA
except:
    pass
