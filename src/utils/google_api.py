import logging
import os
import pickle
from datetime import datetime

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import boto3

from src import settings

logger = logging.getLogger()

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/drive.metadata.readonly",
]


def get_credentials():
    if not settings.DEBUG and not os.path.isfile(settings.GOOGLE_API_CLIENT_SECRET_PATH):
        _download_client_secret_file()
    basepath = os.path.split(os.path.realpath(__file__))[0]
    credential_path = os.path.join(basepath, "credential.pickle")
    credentials = None
    if os.path.exists(credential_path):
        with open(credential_path, "rb") as token:
            credentials = pickle.load(token)
    if not credentials:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                settings.GOOGLE_API_CLIENT_SECRET_PATH, SCOPES
            )
            credentials = flow.run_local_server()
        with open(credential_path, "wb") as token:
            pickle.dump(credentials, token)
    return credentials


def _download_client_secret_file():
    try:
        os.makedirs("/tmp/config")
        s3 = boto3.resource("s3")
        bucket = s3.Bucket(settings.S3_BUCKET_NAME)
        bucket.download_file("config/client_secret.json", settings.GOOGLE_API_CLIENT_SECRET_PATH)
        logger.info("Download S3 config/client_secret.json")
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
