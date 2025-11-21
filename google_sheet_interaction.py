from typing import Any

import gspread
from oauth2client.service_account import ServiceAccountCredentials


def read_tasks_from_sheet(account_file: str, sheet_name: str, sheet_tab: str) -> list[dict[str, Any]]:
    """
    Read rows from Google Sheets and convert them into a list of dicts.

    We assume:
    Row 1 (A1..E1) is header like:
        | site_url | login | password | action | extra_param |
    Row 2+ has actual data.

    We'll read A2:E (GOOGLE_SHEET_RANGE) and zip with headers.
    Adjust headers/range to match your sheet.
    """
    scope = [
        "https://www.googleapis.com/auth/spreadsheets.readonly",
        "https://www.googleapis.com/auth/drive.readonly",
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_name(
        account_file,
        scopes=scope,
    )

    gc = gspread.authorize(creds)

    sh = gc.open(sheet_name)
    ws = sh.worksheet(sheet_tab)

    header = ws.row_values(1)
    print("Header:", header)

    rows = ws.get_all_values()[1:]  # everything except first row
    print("Rows:")
    for r in rows:
        print(r)

    tasks = []
    for row in rows:
        padded = row + [""] * (len(header) - len(row))
        tasks.append(dict(zip(header, padded)))

    print("\nParsed tasks:")
    for t in tasks:
        print(t)

    return tasks