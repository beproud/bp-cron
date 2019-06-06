from src.utils.google_api import get_service


def get_all_values(sheet_id, sheet_name):
    """
    指定したスプレッドシートの全値を返す

    * https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/get
    * https://developers.google.com/resources/api-libraries/documentation/sheets/v4/python/latest/sheets_v4.spreadsheets.values.html#get  # NOQA

    :param sheet_id: スプレッドシートのId
    :param sheet_name: シートの名前
    """
    # Sheets APIに接続
    service = get_service("sheets", "v4")

    # スプレッドシートの情報を取得
    result = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=sheet_id, range=sheet_name)
        .execute()
    )
    return result.get("values", [])
