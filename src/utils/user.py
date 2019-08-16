import logging
import os
from configparser import ConfigParser, NoSectionError

import boto3

from src import settings

logger = logging.getLogger()

SECTION_NAME = "Google account to Slack username"


def gaccount_to_slack(google_account, mention=True):
    """
    google account(XXXX@beproud.jp) を slack の username に変換する

    :param google_account: Googleアカウント
    :param mention: Trueの場合にusernameの前に '@' を付けて返す
    """
    logger.debug("gaccount_to_slack: %s", google_account)
    conf = ConfigParser()
    # 本番環境 and user.iniが存在しない場合、S3からダウンロード
    if not settings.DEBUG and not os.path.isfile(settings.USER_INFO_PATH):
        _download_userconfig_file()

    files = conf.read(settings.USER_INFO_PATH)
    if not files:
        raise FileNotFoundError
    if not conf.has_section(SECTION_NAME):
        raise NoSectionError(SECTION_NAME)
    username = conf[SECTION_NAME].get(google_account, google_account)
    username = username.replace("@beproud.jp", "")
    if mention:
        username = "@" + username
    return username


def _download_userconfig_file():
    """ユーザー名とメールアドレスをマッピングしたファイルを/tmpにダウンロード

    Ref: https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/limits.html
    """
    if not os.path.isdir("/tmp/config"):
        os.makedirs("/tmp/config")
    try:
        s3 = boto3.resource("s3")
        bucket = s3.Bucket(settings.S3_BUCKET_NAME)
        bucket.download_file("config/user.ini", settings.USER_INFO_PATH)
        logger.info("Download S3 config/user.ini")
    except Exception as e:
        # TODO: Error handling
        logger.info(e)
