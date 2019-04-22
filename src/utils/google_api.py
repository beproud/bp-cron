import os
from datetime import datetime
import httplib2

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
# from google_auth_oauthlib.flow import Flow
# from google_auth_oauthlib.flow import InstalledAppFlow

# from src import settings

SCOPES = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/drive.metadata.readonly',
]
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'bp-cron'


# def get_credentials():
#     """
#     credentialsファイルが存在しない場合は認証処理を行って生成する
#     """
#     credential_path = settings.CREDENTIAL_PATH
#     print(f'credential_path:{credential_path}')
#     print(store)
#     store = Storage(credential_path)
#     credentials = store.get()
#     if not credentials or credentials.invalid:
#         flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
#         flow.user_agent = APPLICATION_NAME
#         credentials = tools.run_flow(flow, store)
#         print('credentialsを{}に保存しました'.format(credential_path))
#     return credentials


def get_credentials():
    basepath = os.path.split(os.path.realpath(__file__))[0]
    path = os.path.join(basepath, 'credentials.json')
    f = open(path, 'rb')
    content = f.read()
    credentials = client.Credentials.new_from_json(content)
    return credentials


def get_service(name, version):
    """
    サービスを取得する
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build(name, version, http=http)
    return service


def main():
    service = get_service('calendar', 'v3')

    now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('直近の5件のイベントを表示')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=5, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


if __name__ == '__main__':
    main()
