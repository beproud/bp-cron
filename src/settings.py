DEBUG = False

BOT_EMOJI = ':robot_face:'
BOT_NAME = 'bp-cron'

# Google API の credentials の保存場所
CREDENTIAL_PATH = 'credentials.json'

try:
    from bpcron_settings import * # NOQA
except:
    pass
