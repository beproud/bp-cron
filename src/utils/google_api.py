import logging
import os
import sys
import pickle
from datetime import datetime

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import boto3

# TODO: lambdaにStage環境用意したら消す
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from src import settings ## NOQA

logger = logging.getLogger()

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/drive.metadata.readonly",
]


def get_credentials():

    # lambda環境かつ、/tmp/直下にGoogle APIアクセスに必要なファイルがなければs3からダウンロード
    if not settings.DEBUG and not os.path.isfile(settings.GOOGLE_API_CLIENT_SECRET_PATH):
        _download_google_api_auth_files()

    credentials = None
    if os.path.exists(settings.GOOGLE_API_CREDENTIAL_PATH):
        with open(settings.GOOGLE_API_CREDENTIAL_PATH, "rb") as token:
            credentials = pickle.load(token)
    if not credentials:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                settings.GOOGLE_API_CLIENT_SECRET_PATH, SCOPES
            )
            credentials = flow.run_local_server()
        with open(settings.GOOGLE_API_CREDENTIAL_PATH, "wb") as token:
            pickle.dump(credentials, token)
    return credentials


def _download_google_api_auth_files():
    """ s3に置いたGooleAPI認証ファイルをダウンロードする """
    if not os.path.isdir("/tmp/config"):
        os.makedirs("/tmp/config")
    try:
        s3 = boto3.resource("s3")
        bucket = s3.Bucket(settings.S3_BUCKET_NAME)
        bucket.download_file("config/client_secret.json", settings.GOOGLE_API_CLIENT_SECRET_PATH)
        logger.info("Download S3 config/client_secret.json")
        bucket.download_file("config/credential.pickle", settings.GOOGLE_API_CREDENTIAL_PATH)
        logger.info("Download S3 config/credential.pickle")
    except Exception as e:
        # TODO: Error handling
        logger.info(e)


def get_service(name, version):
    """
    サービスを取得する
    """
    credentials = get_credentials()
    # ref https://github.com/googleapis/google-api-python-client/issues/299
    service = build(name, version, credentials=credentials, cache_discovery=False)
    return service


def main():
    service = get_service("calendar", "v3")

    now = datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    print("直近の5件のイベントを表示")
    eventsResult = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=5,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = eventsResult.get("items", [])

    if not events:
        print("No upcoming events found.")
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        print(start, event["summary"])


if __name__ == "__main__":
    main()
