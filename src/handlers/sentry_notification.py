import os
import logging
import json
from urllib.parse import urlparse

from src.utils import slack

logger = logging.getLogger()


def get_browser_info(event):
    browser = event["contexts"]["browser"]
    if browser is None:
        return "unknown"
    return "{name} {type} {version}".format(**browser)


def get_os_info(event):
    client_os = event["contexts"]["client_os"]
    if client_os is None:
        return "unknown"
    return "{name} {type} {version}".format(**client_os)


def get_slack_channel_name(sentry_url):
    notify_list = os.getenv("SENTRY_NOTIFY_LIST")
    o = urlparse(sentry_url)
    for w in notify_list.split(","):
        sentry_organization_name, channel = w.split("#")
        if sentry_organization_name == o.path.split("/")[2]:
            return "#" + channel


def job(event, context):
    """SentryのWebhookを受けて環境変数に登録されているSlackチャンネルに通知を飛ばす
    """
    logger.info("Start job")
    body = json.loads(event["body"])
    event = body["event"]

    channel = get_slack_channel_name(body["url"])
    if not channel:
        logger.info("Not found Slack Channel")

    browser_info = get_browser_info(event)
    os_info = get_os_info(event)
    title = event["title"] or ""
    environment = event["environment"] or ""
    level = event["level"] or ""
    timestamp = event["timestamp"] or ""
    attachments = [
        {
            "title": title,
            "title_link": body["url"],
            "color": "#CE1515",
            "fields": [
                {
                    "title": "Environment",
                    "value": environment,
                },
                {
                    "title": "Level",
                    "value": level,
                },
                {
                    "title": "Browser Info",
                    "value": browser_info,
                },
                {
                    "title": "ClientOS Info",
                    "value": os_info,
                },
            ],
            "footer": "Send from bp-cron",
            "ts": timestamp,
        }
    ]
    slack.post_message(channel, "Sentry Notify", attachments=attachments)
    logger.info("End job")
