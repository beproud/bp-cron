import logging
import os
from configparser import ConfigParser, NoSectionError

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
    if not os.path.isfile(settings.USER_CONFIG_PATH):
        raise FileNotFoundError
    conf.read(settings.USER_CONFIG_PATH)
    if not conf.has_section(SECTION_NAME):
        raise NoSectionError(SECTION_NAME)
    username = conf[SECTION_NAME].get(google_account, google_account)
    username = username.replace("@beproud.jp", "")
    if mention:
        username = "@" + username
    return username
