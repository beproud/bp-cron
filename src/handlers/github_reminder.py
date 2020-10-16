from collections import defaultdict
from datetime import date
from itertools import count, product
from string import ascii_uppercase
from urllib.parse import urlparse

from github import Github
from slacker import Error

from src import settings
from src.utils import slack
from src.utils.google_api import get_service

BOT_EMOJI = ":github:"
CHANNEL = "#bp-employees"


def add_alpha_prefix(length):
    """セルのアルファベット文字列を返すジェネレータ
    A, B, ..., Y, Z, AA, AB, ..., AY, AZ, BA, ...
    """
    repeat = count(1)
    while True:
        for strs in product(ascii_uppercase, repeat=next(repeat)):
            if length <= 0:
                return
            length -= 1
            yield "".join(strs)


def make_sheet(service, spreadsheet_id, sheet_name, row_count, column_count):
    requests = []
    requests.append(
        {
            "addSheet": {
                "properties": {
                    "title": sheet_name,
                    "index": "0",
                    "gridProperties": {
                        "rowCount": row_count,
                        "columnCount": column_count,
                    },
                }
            }
        }
    )

    body = {"requests": requests}
    response = (
        service.spreadsheets()
        .batchUpdate(spreadsheetId=spreadsheet_id, body=body)
        .execute()
    )
    return response


def write_sheet(
    service,
    spreadsheet_id,
    sheet_name,
    row_count,
    column_count,
    org_member_to_repos,
    col_member_to_repos,
):

    alpha_prefix = [p for p in add_alpha_prefix(row_count)]
    start, end = alpha_prefix[0], alpha_prefix[-1]
    _range = sheet_name + f"!{start}1:{end}{column_count}"
    body = {}
    body["range"] = _range
    body["majorDimension"] = "ROWS"

    values = []
    values.append([f"組織メンバー:{len(org_member_to_repos)}"])
    for m, repo in org_member_to_repos.items():
        inner_list = []
        inner_list.append(m)
        inner_list.extend(repo)
        values.append(inner_list)

    values.append([])  # 一行開ける
    values.append([f"組織外メンバー:{len(col_member_to_repos)}"])
    for m, repo in col_member_to_repos.items():
        inner_list = []
        inner_list.append(m)
        inner_list.extend(repo)
        values.append(inner_list)

    body["values"] = values

    value_input_option = "USER_ENTERED"
    result = (
        service.spreadsheets()
        .values()
        .update(
            spreadsheetId=spreadsheet_id,
            range=_range,
            valueInputOption=value_input_option,
            body=body,
        )
        .execute()
    )
    return result


def fetch_organization_repostiries_info():
    g = Github(settings.GITHUB_API_TOKEN)

    org = g.get_organization(settings.GITHUB_ORGANIZATION)
    # プライベートリポジトリ
    org_private_repos = list(org.get_repos(type="private"))
    org_private_repos_number = len(org_private_repos)

    # 組織メンバー
    org_members = sorted(org.get_members(), key=lambda m: m.login)
    # 組織外メンバー:
    col_members = sorted(org.get_outside_collaborators(), key=lambda m: m.login)

    cm = defaultdict(list)
    for r in org_private_repos:
        for m in r.get_collaborators():
            cm[m.login].append(r.full_name)

    org_member_to_repos = {m.login: cm[m.login] for m in org_members}

    col_member_to_repos = {m.login: cm[m.login] for m in col_members}
    return org_private_repos_number, org_member_to_repos, col_member_to_repos


def notify_member_check(event, context):
    service = get_service("sheets", "v4")
    result = urlparse(settings.GITHUB_SPREADSHEET_URL)
    sheet_id = result.path.split("/")[3]
    org_private_repos_number, org_member_to_repos, col_member_to_repos = (
        fetch_organization_repostiries_info()
    )
    # 3 -> メンバ名列 + 余白分の行を追加
    row_count = 3 + org_private_repos_number
    # 10 -> 総数を記載する行の数 + 余白分の行を追加
    column_count = 10 + len(org_member_to_repos) + len(org_member_to_repos)
    sheet_name = f"{date.today().month}月"
    make_sheet(service, sheet_id, sheet_name, row_count, column_count)
    write_sheet(
        service,
        sheet_id,
        sheet_name,
        row_count,
        column_count,
        org_member_to_repos,
        col_member_to_repos,
    )

    try:
        slack.post_message(
            CHANNEL,
            ":octocat: < @here GitHubメンバー整理をしよう",
            username="GitHub Information Bot",
            icon_emoji=BOT_EMOJI,
            attachments=[{
                "pretext": "案件のリポジトリを確認してGitHubを利用していないメンバーがいたら外しましょう。",
                "color": "#e83a3a",
                "text": f"<{settings.GITHUB_SPREADSHEET_URL}|メンバー一覧>"
            }],
            link_names=True,
        )
    except Error:
        pass
