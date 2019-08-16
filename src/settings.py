import logging
import os

# logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

DEBUG = False

# Slack settings

# Create token https://api.slack.com/docs/oauth-test-tokens
SLACK_TOKEN = os.environ['SLACK_API_TOKEN']

BOT_EMOJI = ':robot_face:'
BOT_NAME = 'bp-cron'

# S3 バケット名
S3_BUCKET_NAME = "bp-cron-serverless-deployment"
# S3 設定ファイルが格納されているフォルダ
CONFIG_PATH = os.path.join("/tmp", "config")

# ユーザー情報の設定ファイル
USER_INFO_PATH = os.path.join(CONFIG_PATH, "user.ini")

# Google API
GOOGLE_API_CLIENT_SECRET_PATH = os.path.join(CONFIG_PATH, "client_secret.json")
GOOGLE_API_CREDENTIAL_PATH = os.path.join(CONFIG_PATH, "credential.pickle")

# TODO fix
try:
    from src.bpcron_settings import * # NOQA
except Exception:
    pass
